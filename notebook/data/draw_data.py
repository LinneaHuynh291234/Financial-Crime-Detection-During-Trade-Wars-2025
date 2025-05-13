import random
import uuid
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker
fake = Faker()
nordic_countries = ['SE', 'FI', 'DK', 'NO']
currencies = {'SE': 'SEK', 'FI': 'EUR', 'DK': 'DKK', 'NO': 'NOK'}
business_types = ['Textile', 'Electronics', 'Shipping', 'Agriculture', 'Consulting']
swift_codes = ['NDEASESS', 'DABADKKK', 'NOKANO21', 'HANDFIHH']

# Generate fake transaction
def generate_transaction():
    from_country = random.choice(nordic_countries)
    counter_country = random.choice(['HK', 'CN', 'US', 'SE', 'DE', 'FI', 'DK', 'NO'])
    invoice_id = fake.uuid4() if random.random() > 0.7 else ''

    transaction_date = fake.date_between(start_date=datetime(2025, 4, 2), end_date=datetime(2025, 12, 31))
    booking_date = transaction_date + timedelta(days=random.randint(0, 2))
    value_date = booking_date + timedelta(days=random.randint(0, 1))
    payment_date = value_date + timedelta(days=random.randint(0, 3))

    return {
        'transaction_id': str(uuid.uuid4()),
        'transaction_date': transaction_date,
        'booking_date': booking_date,
        'value_date': value_date,
        'payment_date': payment_date,
        'amount': round(random.uniform(100, 500000), 2),
        'currency': currencies[from_country],
        'from_account_id': fake.iban(),
        'from_account_name': fake.company(),
        'from_account_country': from_country,
        'from_account_business_type': random.choice(business_types),
        'from_account_expected_turnover': round(random.uniform(50000, 2000000), 2),
        'counterparty_account_id': fake.iban(),
        'counterparty_name': fake.company(),
        'counterparty_country': counter_country,
        'counterparty_bank_bic': random.choice(swift_codes),
        'counterparty_business_type': random.choice(business_types),
        'narrative': fake.bs(),
        'payment_purpose_code': random.choice(['Invoice', 'Salary', 'Goods', 'Consulting', 'Unknown']),
        'related_trade_invoice_id': invoice_id,
        'swift_message_type': random.choice(['MT103', 'MT202', 'MT940']),
        'transaction_status': random.choice(['billed', 'pending', 'failed']),
        'transaction_type_description': random.choice(['BG-LI-LÖN', 'Wire Transfer', 'Card Payment', 'Direct Debit']),
        'end_to_end_identification': str(uuid.uuid4()) if random.random() > 0.5 else ''
    }

# Create base dataset
data = [generate_transaction() for _ in range(9500)]

# Introduce some missing values
for record in data:
    if random.random() < 0.05:
        record['counterparty_name'] = ''
    if random.random() < 0.05:
        record['narrative'] = ''
    if random.random() < 0.03:
        record['from_account_business_type'] = ''

# Add duplicates
data.extend(random.sample(data, 200))

# Convert to DataFrame
df = pd.DataFrame(data)

# Inject fraud including structuring
def inject_fraud(df, num_fraud_cases=300, structured_cases=50):
    fraud_cases = []
    risky_countries = ['HK', 'SG', 'CN', 'RU']

    # Structuring: split payments
    for _ in range(structured_cases):
        from_country = random.choice(nordic_countries)
        counter_country = random.choice(risky_countries)
        base_invoice_id = str(uuid.uuid4())
        base_amount = round(random.uniform(200000, 400000), 2)
        num_parts = random.randint(5, 10)
        split_amounts = [round(base_amount / num_parts, 2) for _ in range(num_parts)]
        split_amounts[-1] += round(base_amount - sum(split_amounts), 2)

        base_date = fake.date_between(start_date=datetime(2025, 4, 2), end_date=datetime(2025, 12, 15))

        for i in range(num_parts):
            transaction_date = base_date + timedelta(days=i % 3)
            booking_date = transaction_date + timedelta(days=random.randint(0, 1))
            value_date = booking_date + timedelta(days=random.randint(0, 1))
            payment_date = value_date + timedelta(days=random.randint(0, 2))

            fraud_cases.append({
                'transaction_id': str(uuid.uuid4()),
                'transaction_date': transaction_date,
                'booking_date': booking_date,
                'value_date': value_date,
                'payment_date': payment_date,
                'amount': split_amounts[i],
                'currency': 'USD',
                'from_account_id': fake.iban(),
                'from_account_name': fake.company(),
                'from_account_country': from_country,
                'from_account_business_type': 'Consulting',
                'from_account_expected_turnover': round(random.uniform(50000, 80000), 2),
                'counterparty_account_id': fake.iban(),
                'counterparty_name': fake.company(),
                'counterparty_country': counter_country,
                'counterparty_bank_bic': random.choice(swift_codes),
                'counterparty_business_type': 'Electronics',
                'narrative': "Payment for services",
                'payment_purpose_code': 'Goods',
                'related_trade_invoice_id': base_invoice_id,
                'swift_message_type': 'MT103',
                'transaction_status': 'billed',
                'transaction_type_description': 'Wire Transfer',
                'end_to_end_identification': str(uuid.uuid4())
            })

    # Regular fraud cases
    for _ in range(num_fraud_cases - structured_cases):
        transaction_date = fake.date_between(start_date=datetime(2025, 4, 2), end_date=datetime(2025, 12, 31))
        booking_date = transaction_date + timedelta(days=random.randint(0, 2))
        value_date = booking_date + timedelta(days=random.randint(0, 1))
        payment_date = value_date + timedelta(days=random.randint(0, 3))

        fraud_cases.append({
            'transaction_id': str(uuid.uuid4()),
            'transaction_date': transaction_date,
            'booking_date': booking_date,
            'value_date': value_date,
            'payment_date': payment_date,
            'amount': round(random.uniform(100000, 500000), 2),
            'currency': random.choice(['EUR', 'USD', 'SEK']),
            'from_account_id': fake.iban(),
            'from_account_name': fake.company(),
            'from_account_country': random.choice(nordic_countries),
            'from_account_business_type': random.choice(['Textile', 'Consulting']),
            'from_account_expected_turnover': round(random.uniform(50000, 100000), 2),
            'counterparty_account_id': fake.iban(),
            'counterparty_name': fake.company(),
            'counterparty_country': random.choice(risky_countries),
            'counterparty_bank_bic': random.choice(swift_codes),
            'counterparty_business_type': random.choice(['Electronics', 'Shipping']),
            'narrative': "Invoice for electronic parts",
            'payment_purpose_code': 'Goods',
            'related_trade_invoice_id': '',
            'swift_message_type': 'MT103',
            'transaction_status': 'billed',
            'transaction_type_description': 'Wire Transfer',
            'end_to_end_identification': str(uuid.uuid4())
        })

    fraud_df = pd.DataFrame(fraud_cases)
    df_with_fraud = pd.concat([df, fraud_df], ignore_index=True)
    return df_with_fraud

# Inject fraud
df_with_fraud = inject_fraud(df)

# Add label
df_with_fraud['is_fraud'] = 0
df_with_fraud.iloc[-300:, df_with_fraud.columns.get_loc('is_fraud')] = 1

# Shuffle
df_with_fraud = df_with_fraud.sample(frac=1, random_state=42).reset_index(drop=True)

# Save
df_with_fraud.to_csv('nordic_transactions_with_fraud.csv', index=False)
print("File 'nordic_transactions_with_fraud.csv' generated with fraud cases including structuring.")