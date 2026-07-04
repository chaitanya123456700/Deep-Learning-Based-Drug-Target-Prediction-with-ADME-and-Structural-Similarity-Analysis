import requests
import pandas as pd
import time

# -----------------------------
# TARGET LIST (Correct IDs)
# -----------------------------

TARGETS = {
    "ABL1": "CHEMBL1862",
    "EGFR": "CHEMBL203",
    "VEGFR2": "CHEMBL279",
    "BRAF": "CHEMBL5145",
    "JAK2": "CHEMBL2971",
    "DRD2": "CHEMBL217",
    "HTR2A": "CHEMBL224",
    "ADRB2": "CHEMBL210",
    "COX2": "CHEMBL230",
    "ACHE": "CHEMBL220",
    "HDAC1": "CHEMBL325",
    "MAOA": "CHEMBL1951",
    "ESR1": "CHEMBL206",
    "AR": "CHEMBL1871"
}

BASE_URL = "https://www.ebi.ac.uk/chembl/api/data/activity.json"

def fetch_target_data(target_name, chembl_id, max_records=500):
    print(f"Fetching data for {target_name}...")

    url = f"{BASE_URL}?target_chembl_id={chembl_id}&standard_type=IC50&limit={max_records}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed for {target_name}")
        return []

    data = response.json()["activities"]

    records = []

    for entry in data:
        try:
            ic50 = float(entry["standard_value"])
            smiles = entry["canonical_smiles"]

            if smiles is None:
                continue

            # Label active/inactive
            label = 1 if ic50 <= 1000 else 0

            records.append({
                "SMILES": smiles,
                "Target": target_name,
                "Label": label
            })

        except:
            continue

    print(f"{target_name}: {len(records)} records")
    return records


def build_dataset():
    all_data = []

    for target_name, chembl_id in TARGETS.items():
        records = fetch_target_data(target_name, chembl_id)
        all_data.extend(records)
        time.sleep(1)  # avoid API overload

    df = pd.DataFrame(all_data)

    # Remove duplicates
    df = df.drop_duplicates()

    print("Total records:", len(df))

    df.to_csv("backend/data/raw_chembl_data.csv", index=False)
    print("Raw dataset saved!")


if __name__ == "__main__":
    build_dataset()