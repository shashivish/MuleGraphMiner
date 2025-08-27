from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

fake = Faker()

def generate_synthetic_transactions_with_overlap(
        num_campaigns=2,
        externals_per_campaign=4,
        internals_per_campaign=4,
        beneficiaries_per_campaign=2):
    records = []
    base_time = datetime.now()

    # Generate global beneficiary pool to share across campaigns
    all_beneficiaries = [f'B{i+1}' for i in range(num_campaigns * beneficiaries_per_campaign)]
    all_beneficiary_names = [fake.company() for _ in range(num_campaigns * beneficiaries_per_campaign)]

    # Map beneficiary index to name for easy lookup
    beneficiary_map = dict(zip(all_beneficiaries, all_beneficiary_names))

    for c in range(num_campaigns):
        company_name = fake.company()
        externals = [fake.bban() for _ in range(externals_per_campaign)]
        internals = [f'I{c*internals_per_campaign + i + 1}' for i in range(internals_per_campaign)]
        # Instead of separate per-campaign beneficiaries, pick across full pool for overlap
        beneficiary_indices_for_campaign = random.sample(range(len(all_beneficiaries)), beneficiaries_per_campaign)
        beneficiaries = [all_beneficiaries[i] for i in beneficiary_indices_for_campaign]
        beneficiary_names = [beneficiary_map[b] for b in beneficiaries]

        # Generate unique fake company name per internal account (consistent)
        internal_company_names = {int_acc: fake.company() for int_acc in internals}

        # Ingress phase: externals to internals
        for ext in externals:
            for int_acc in internals:
                amount = round(random.uniform(1000, 10000), 2)
                timestamp = base_time + timedelta(minutes=random.randint(0, 60))
                records.append({
                    "Originator_Name": company_name,
                    "Originator_Account": ext,
                    "Originator_Type": "External",
                    "Beneficiary_Name": internal_company_names[int_acc],
                    "Beneficiary_Account": int_acc,
                    "Beneficiary_Type": "Internal",
                    "Amount": amount,
                    "Timestamp": timestamp
                })

        # Egress phase: internals to beneficiaries (possibly from other campaigns)
        for int_acc in internals:
            # Select beneficiaries randomly from the full global beneficiary pool for overlap
            chosen_beneficiaries = random.sample(all_beneficiaries, random.randint(1, beneficiaries_per_campaign + 1))
            for ben in chosen_beneficiaries:
                amount = round(random.uniform(500, 9000), 2)
                timestamp = base_time + timedelta(minutes=random.randint(61, 120))
                records.append({
                    "Originator_Name": internal_company_names[int_acc],
                    "Originator_Account": int_acc,
                    "Originator_Type": "Internal",
                    "Beneficiary_Name": beneficiary_map[ben],
                    "Beneficiary_Account": ben,
                    "Beneficiary_Type": "Beneficiary",
                    "Amount": amount,
                    "Timestamp": timestamp
                })

    df = pd.DataFrame(records)
    return df

df = generate_synthetic_transactions_with_overlap()
df.to_csv("../../data/synthetic_transactions_overlap.csv", index=False)
print(df.head(20))
