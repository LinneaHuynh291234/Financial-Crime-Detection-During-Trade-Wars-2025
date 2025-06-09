import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker(["sv_SE", "en_US", "fi_FI", "no_NO", "da_DK", "nl_NL"])
Faker.seed(42)
random.seed(42)
np.random.seed(42)

NUM_CUSTOMERS = 1000
NUM_TRANSACTIONS = 10000
DUPLICATE_RATIO = 0.1

START_DATE = datetime(2025, 4, 2)
END_DATE = datetime(2025, 7, 2)

non_sanctioned_countries = ["SE", "NO", "FI", "DK", "NL"]

country_currency_map = {
    "SE": "SEK",
    "NO": "NOK",
    "FI": "EUR",
    "DK": "DKK",
    "NL": "EUR"
}

product_choices = ["PERSONKONTO", "SPARKONTO", "STUDENTKONTO"]
account_types = ["Current", "Savings"]

# Bank fixed to Nordea
bank_info = {"name": "Nordea", "bic": "NDEASESS", "country": "SE"}

def random_date(start, end):
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

def generate_ordered_dates():
    # transaction_date ≤ value_date ≤ payment_date ≤ booking_date
    t_date = random_date(START_DATE, END_DATE)
    v_date = t_date + timedelta(days=random.randint(0, 2))
    p_date = v_date + timedelta(days=random.randint(0, 2))
    b_date = p_date + timedelta(days=random.randint(0, 2))
    return [d.strftime("%Y-%m-%d") for d in [t_date, v_date, p_date, b_date]]

def generate_account_numbers():
    base = str(random.randint(40000000000, 49999999999))
    bban = base
    iban = f"SE80{str(3000000000 + int(base[-10:]))}"
    return [
        {"value": bban, "_type": "BBAN_SE"},
        {"value": iban, "_type": "IBAN"}
    ]

def generate_customers(n):
    customers = []
    for i in range(n):
        customer_id = f"CUST{i:05d}"
        account_numbers = generate_account_numbers()
        country = random.choice(non_sanctioned_countries)
        currency = country_currency_map[country]
        account_name = fake.name()
        product = random.choice(product_choices)
        account_type = random.choice(account_types)
        available_balance = round(random.uniform(500, 150000), 2)
        value_dated_balance = round(available_balance * random.uniform(0.5, 1.0), 2)
        credit_limit = round(random.uniform(500, 20000), 2)
        latest_booking = END_DATE.strftime("%Y-%m-%d")

        customers.append({
            "customer_id": customer_id,
            "country": country,
            "account_numbers": account_numbers,
            "currency": currency,
            "account_name": account_name,
            "product": product,
            "account_type": account_type,
            "available_balance": f"{available_balance:.2f}",
            "booked_balance": f"{available_balance:.2f}",
            "value_dated_balance": f"{value_dated_balance:.2f}",
            "bank": bank_info,
            "status": "OPEN",
            "credit_limit": f"{credit_limit:.2f}",
            "latest_transaction_booking_date": latest_booking,
            "registration_number": fake.ssn()
        })
    return pd.json_normalize(customers)

def generate_detailed_transactions(customer_ids, customers_df, n):
    data = []
    types = [
        ("Kortköp", "Card payment at {merchant}", "card"),
        ("Swish", "Swish payment to {merchant}", "swish"),
        ("Autogiro", "Direct debit to {merchant}", "autogiro"),
        ("Överföring", "Transfer to {merchant}", "transfer"),
        ("Insättning", "Deposit from {merchant}", "deposit")
    ]

    credit_limit_map = dict(zip(customers_df.customer_id, customers_df.credit_limit.astype(float)))
    currency_map = dict(zip(customers_df.customer_id, customers_df.currency))

    for _ in range(int(n * (1 - DUPLICATE_RATIO))):
        cid = random.choice(customer_ids)
        t_type = random.choice(types)
        merchant = fake.company()
        max_amount = credit_limit_map[cid]
        amount = round(random.uniform(10, max_amount), 2)
        t_date, v_date, p_date, b_date = generate_ordered_dates()
        currency = currency_map[cid]

        tx = {
            "customer_id": cid,
            "transaction_id": fake.uuid4(),
            "currency": currency,
            "booking_date": b_date,
            "value_date": v_date,
            "transaction_date": t_date,
            "payment_date": p_date,
            "type_description": t_type[0],
            "narrative": t_type[1].format(merchant=merchant),
            "status": "billed",
            "counterparty_name": merchant,
            "amount": f"{amount:.2f}"
        }

        if t_type[2] == "card":
            tx["card_number"] = " ".join(str(random.randint(1000, 9999)) for _ in range(4))
        elif t_type[2] == "swish":
            tx["message"] = "Membership payment"
            tx["own_message"] = "Sports club 2025"

        data.append(tx)

    duplicates = random.choices(data, k=int(n * DUPLICATE_RATIO))
    data.extend(duplicates)
    return pd.DataFrame(data)

def generate_summaries(transactions, customers_df):
    transactions["amount_f"] = transactions["amount"].astype(float)
    summaries = transactions.groupby("customer_id").agg(
        total_volume=('amount_f', 'sum'),
        avg_amount=('amount_f', 'mean'),
        max_amount=('amount_f', 'max'),
        min_amount=('amount_f', 'min'),
        transaction_count=('transaction_id', 'count'),
        last_transaction_date=('transaction_date', 'max')
    ).reset_index()

    cust_info = customers_df[["customer_id", "available_balance", "credit_limit", "country", "currency"]].copy()
    cust_info["available_balance"] = cust_info["available_balance"].astype(float)
    cust_info["credit_limit"] = cust_info["credit_limit"].astype(float)

    summaries = summaries.merge(cust_info, on="customer_id", how="left")

    for col in ["total_volume", "avg_amount", "max_amount", "min_amount", "available_balance", "credit_limit"]:
        summaries[col] = summaries[col].round(2)

    return summaries

# Generate data

customers_df = generate_customers(NUM_CUSTOMERS)
transactions_df = generate_detailed_transactions(customers_df["customer_id"].tolist(), customers_df, NUM_TRANSACTIONS)
summaries_df = generate_summaries(transactions_df, customers_df)

# Save files

customers_df.to_csv("customers.csv", index=False)
transactions_df.to_csv("transactions.csv", index=False)
summaries_df.to_csv("summaries.csv", index=False)

print("✅ Generated customers.csv, transactions.csv, summaries.csv with dynamic currency and updated logic.")
