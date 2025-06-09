import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# -----------------------------------------------------------------------------
#  Configuration
# -----------------------------------------------------------------------------
fake = Faker(["sv_SE", "en_US", "fi_FI", "no_NO", "da_DK", "nl_NL"])
Faker.seed(42)
random.seed(42)
np.random.seed(42)

NUM_CUSTOMERS      = 1_000
NUM_TRANSACTIONS   = 10_717
DUPLICATE_RATIO    = 0.01      # 1 % duplicate transactions

START_DATE = datetime(2025, 4, 2)
END_DATE   = datetime(2025, 7, 2)

non_sanctioned_countries = ["SE", "NO", "FI", "DK", "NL"]
country_currency_map = {"SE": "SEK", "NO": "NOK", "FI": "EUR", "DK": "DKK", "NL": "EUR"}

product_choices = ["PERSONKONTO", "SPARKONTO", "STUDENTKONTO"]
account_types   = ["Current", "Savings"]
occupations     = ["Engineer", "Doctor", "Teacher", "Consultant", "Cashier",
                   "Artist", "Driver", "Student", "Analyst", "Nurse"]
genders         = ["Male", "Female", "Other"]

# Bank fixed to Nordea but country varies per customer
def random_bank():
    return {"name": "Nordea", "bic": "NDEASESS",
            "country": random.choice(non_sanctioned_countries)}

# -----------------------------------------------------------------------------
#  Helper functions
# -----------------------------------------------------------------------------
def random_datetime(start, end):
    """Return a random timestamp string between start and end."""
    delta_seconds = int((end - start).total_seconds())
    rand_dt = start + timedelta(seconds=random.randint(0, delta_seconds))
    return rand_dt.strftime("%Y-%m-%d %H:%M:%S")

def ordered_datetimes():
    """Generate four timestamps in chronological order."""
    t  = random_datetime(START_DATE, END_DATE)
    t0 = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")

    v  = (t0 + timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d %H:%M:%S")
    v0 = datetime.strptime(v, "%Y-%m-%d %H:%M:%S")

    p  = (v0 + timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d %H:%M:%S")
    p0 = datetime.strptime(p, "%Y-%m-%d %H:%M:%S")

    b  = (p0 + timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d %H:%M:%S")
    return t, v, p, b

def account_numbers():
    """Return BBAN + IBAN pair for Sweden‑style accounts."""
    base = str(random.randint(40000000000, 49999999999))
    return [
        {"value": base, "_type": "BBAN_SE"},
        {"value": f"SE80{3000000000 + int(base[-10:])}", "_type": "IBAN"}
    ]

# -----------------------------------------------------------------------------
#  1. Customers
# -----------------------------------------------------------------------------
def generate_customers(n):
    rows = []
    for i in range(n):
        cust_id  = f"CUST{i:05d}"
        country  = random.choice(non_sanctioned_countries)
        currency = country_currency_map[country]
        balance  = round(random.uniform(500, 150_000), 2)

        rows.append({
            "customer_id"                 : cust_id,
            "country"                     : country,
            "currency"                    : currency,
            "account_numbers"             : account_numbers(),
            "account_name"                : fake.name(),
            "product"                     : random.choice(product_choices),
            "account_type"                : random.choice(account_types),
            "available_balance"           : f"{balance:.2f}",
            "booked_balance"              : f"{balance:.2f}",
            "value_dated_balance"         : f"{balance * random.uniform(0.5,1.0):.2f}",
            "bank"                        : random_bank(),
            "status"                      : "OPEN",
            "credit_limit"                : f"{random.uniform(500, 20_000):.2f}",
            "latest_transaction_booking_date": END_DATE.strftime("%Y-%m-%d"),
            "registration_number"         : fake.ssn(),
            # --- new KYC columns ---
            "dob": fake.date_of_birth(minimum_age=18, maximum_age=75).strftime("%Y-%m-%d"),
            "nationality"       : country,
            "residence_country" : random.choice(non_sanctioned_countries),
            "occupation"        : random.choice(occupations),
            "gender"            : random.choice(genders)
        })
    return pd.json_normalize(rows)

# -----------------------------------------------------------------------------
#  2. Transactions
# -----------------------------------------------------------------------------
def generate_transactions(cust_df, n):
    rows = []
    types = [
        ("Kortköp",     "card",      "Card payment at {m}"),
        ("Swish",       "swish",     "Swish payment to {m}"),
        ("Autogiro",    "autogiro",  "Direct debit to {m}"),
        ("Överföring",  "transfer",  "Transfer to {m}"),
        ("Insättning",  "deposit",   "Deposit from {m}")
    ]

    credit_map  = dict(zip(cust_df.customer_id, cust_df.credit_limit.astype(float)))
    currency_map= dict(zip(cust_df.customer_id, cust_df.currency))

    # unique + duplicate part
    for _ in range(int(n * (1 - DUPLICATE_RATIO))):
        cid             = random.choice(cust_df.customer_id)
        type_desc, ttype, narr_fmt = random.choice(types)
        merchant        = fake.company()
        amount          = round(random.uniform(10, credit_map[cid]), 2)
        t_date, v_date, p_date, b_date = ordered_datetimes()
        currency        = currency_map[cid]

        row = {
            "customer_id"     : cid,
            "transaction_id"  : fake.uuid4(),
            "currency"        : currency,
            "transaction_date": t_date,
            "value_date"      : v_date,
            "payment_date"    : p_date,
            "booking_date"    : b_date,
            "type_description": type_desc,
            "transaction_type": ttype,
            "narrative"       : narr_fmt.format(m=merchant),
            "status"          : "billed",
            "counterparty_name": merchant,
            "amount"          : f"{amount:.2f}"
        }
        # conditional extras
        if ttype == "card":
            row["card_number"] = " ".join(str(random.randint(1000, 9999)) for _ in range(4))
        elif ttype == "swish":
            row.update({"message":"Membership payment", "own_message":"Sports club 2025"})
        rows.append(row)

    # add duplicates
    rows.extend(random.choices(rows, k=int(n * DUPLICATE_RATIO)))
    return pd.DataFrame(rows)

# -----------------------------------------------------------------------------
#  3. Summaries
# -----------------------------------------------------------------------------
def kyc_summaries(tx_df, cust_df):
    tx_df["amount_f"] = tx_df["amount"].astype(float)

    agg = (tx_df.groupby("customer_id")
                 .agg(total_volume=('amount_f','sum'),
                      avg_amount  =('amount_f','mean'),
                      max_amount  =('amount_f','max'),
                      min_amount  =('amount_f','min'),
                      transaction_count=('transaction_id','count'),
                      last_transaction_date=('transaction_date','max'))
                 .reset_index())

    cust_cols = ["customer_id","available_balance","credit_limit",
                 "country","currency"]
    merged = agg.merge(cust_df[cust_cols], on="customer_id", how="left")

    # round numeric columns nicely
    for col in ["total_volume","avg_amount","max_amount",
                "min_amount","available_balance","credit_limit"]:
        merged[col] = merged[col].astype(float).round(2)

    return merged

# -----------------------------------------------------------------------------
#  Generate & Save
# -----------------------------------------------------------------------------
customers   = generate_customers(NUM_CUSTOMERS)
transactions= generate_transactions(customers, NUM_TRANSACTIONS)
summaries   = kyc_summaries(transactions, customers)

customers.to_csv("customers.csv",    index=False)
transactions.to_csv("transactions.csv", index=False)
summaries.to_csv("summary_statistics.csv", index=False)

print("✅ customers.csv, transactions.csv, summary_statistics.csv generated.")
