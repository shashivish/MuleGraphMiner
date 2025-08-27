from faker import Faker
import pandas as pd
import random
from datetime import timedelta

fake = Faker()

def add_noise_with_new_entities(df, num_noise=100):
    noise_records = []

    start_time = df['Timestamp'].min()
    end_time = df['Timestamp'].max()
    total_seconds = (end_time - start_time).total_seconds()

    for _ in range(num_noise):
        # Generate fresh fake originator and beneficiary names/accounts
        originator_name = fake.company()
        originator_account = fake.bban()
        beneficiary_name = fake.company()
        beneficiary_account = fake.bban()

        # Randomly assign types to simulate diverse data
        originator_type = random.choice(['External', 'Internal'])
        beneficiary_type = random.choice(['Internal', 'Beneficiary'])

        # Random amount and timestamp within data range
        amount = round(random.uniform(10, 5000), 2)
        random_sec = random.randint(0, int(total_seconds))
        timestamp = start_time + timedelta(seconds=random_sec)

        noise_records.append({
            'Originator_Name': originator_name,
            'Originator_Account': originator_account,
            'Originator_Type': originator_type,
            'Beneficiary_Name': beneficiary_name,
            'Beneficiary_Account': beneficiary_account,
            'Beneficiary_Type': beneficiary_type,
            'Amount': amount,
            'Timestamp': timestamp
        })

    noise_df = pd.DataFrame(noise_records)

    # Append noise transactions to original dataframe and shuffle
    combined_df = pd.concat([df, noise_df], ignore_index=True).sample(frac=1).reset_index(drop=True)
    return combined_df

# Usage example:
df = pd.read_csv('../../data/synthetic_transactions_overlap.csv', parse_dates=['Timestamp'])
df_noisy = add_noise_with_new_entities(df, num_noise=200)
df_noisy.to_csv('../../data/synthetic_with_noise.csv', index=False)
print(df_noisy.tail(10))
