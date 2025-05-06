import pandas as pd
import numpy as np
import random
import uuid
from faker import Faker

# Initialize Faker
fake = Faker()
nordic_countries = ['SE', 'FI', 'DK', 'NO']
currencies = {'SE': 'SEK', 'FI': 'EUR', 'DK': 'DKK', 'NO': 'NOK'}
business_types = ['Textile', 'Electronics', 'Shipping', 'Agriculture', 'Consulting']
swift_codes = ['NDEASESS', 'DABADKKK', 'NOKANO21', 'HANDFIHH']

# Generate fake dataset
def generate_transaction():
    from_country = random.choice(nordic_countries)
    counter_country = random.choice(['HK', 'CN', 'US', 'SE', 'DE', 'FI', 'DK', 'NO'])
    fx_flag = random.choices(['Y', 'N'], weights=[0.2, 0.8])[0]
    invoice_id = fake.uuid4() if random.random() > 0.7 else ''
    return {
        'transaction_id': str(uuid.uuid4()),
        'booking_date': fake.date_between(start_date='-1y', end_date='today'),
        'value_date': fake.date_between(start_date='-1y', end_date='today'),
        'transaction_date': fake.date_between(start_date='-1y', end_date='today'),
        'payment_date': fake.date_between(start_date='-1y', end_date='today'),
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
        'fx_conversion_flag': fx_flag,
        'related_trade_invoice_id': invoice_id,
        'swift_message_type': random.choice(['MT103', 'MT202', 'MT940']),
        'transaction_status': random.choice(['billed', 'pending', 'failed']),
        'transaction_type_description': random.choice(['BG-LI-LÖN', 'Wire Transfer', 'Card Payment', 'Direct Debit']),
        'end_to_end_identification': str(uuid.uuid4()) if random.random() > 0.5 else ''
    }

# Create dataset
data = [generate_transaction() for _ in range(9500)]

# Introduce some missing values
for record in data:
    if random.random() < 0.05:
        record['counterparty_name'] = ''
    if random.random() < 0.05:
        record['narrative'] = ''
    if random.random() < 0.03:
        record['from_account_business_type'] = ''

# Add some duplicate rows
duplicates = random.sample(data, 500)
data.extend(duplicates)

# Convert to DataFrame
df = pd.DataFrame(data)

# Define function to inject fraud
def inject_fraud(df, num_fraud_cases=300):
    fraud_cases = []
    risky_countries = ['HK', 'SG', 'CN', 'RU']
    for _ in range(num_fraud_cases):
        fraud = {
            'transaction_id': str(uuid.uuid4()),
            'booking_date': fake.date_between(start_date='-6m', end_date='today'),
            'value_date': fake.date_between(start_date='-6m', end_date='today'),
            'transaction_date': fake.date_between(start_date='-6m', end_date='today'),
            'payment_date': fake.date_between(start_date='-6m', end_date='today'),
            'amount': round(random.uniform(100000, 500000), 2),  # large amounts
            'currency': random.choice(['EUR', 'USD', 'SEK']),
            'from_account_id': fake.iban(),
            'from_account_name': fake.company(),
            'from_account_country': random.choice(['SE', 'FI', 'DK', 'NO']),
            'from_account_business_type': random.choice(['Textile', 'Consulting']),  # mismatch industries
            'from_account_expected_turnover': round(random.uniform(50000, 100000), 2),  # low turnover
            'counterparty_account_id': fake.iban(),
            'counterparty_name': fake.company(),
            'counterparty_country': random.choice(risky_countries),
            'counterparty_bank_bic': random.choice(swift_codes),
            'counterparty_business_type': random.choice(['Electronics', 'Shipping']),
            'narrative': "Invoice for electronic parts",  # wrong for textile company
            'payment_purpose_code': 'Goods',
            'fx_conversion_flag': 'Y',
            'related_trade_invoice_id': '',
            'swift_message_type': 'MT103',
            'transaction_status': 'billed',
            'transaction_type_description': 'Wire Transfer',
            'end_to_end_identification': str(uuid.uuid4())
        }
        fraud_cases.append(fraud)
    fraud_df = pd.DataFrame(fraud_cases)
    df_with_fraud = pd.concat([df, fraud_df], ignore_index=True)
    return df_with_fraud

# Inject fraud into dataset
df_with_fraud = inject_fraud(df)

# Add "is_fraud" label column
df_with_fraud['is_fraud'] = 0  # Default all normal
df_with_fraud.loc[df_with_fraud.index[-300:], 'is_fraud'] = 1  # Label last 300 as fraud

# Shuffle the dataset
df_with_fraud = df_with_fraud.sample(frac=1, random_state=42).reset_index(drop=True)

# Save new dataset
df_with_fraud.to_csv('nordic_transactions_with_fraud.csv', index=False)
print('CSV file "nordic_fake_transactions_with_fraud.csv" generated with fraud cases included.')