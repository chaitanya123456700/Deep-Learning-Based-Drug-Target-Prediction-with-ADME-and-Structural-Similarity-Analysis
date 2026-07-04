import pandas as pd

RAW_PATH = "backend/data/raw_chembl_data.csv"
OUTPUT_PATH = "backend/data/final_dataset.csv"

def build_multilabel_dataset():
    df = pd.read_csv(RAW_PATH)

    print("Raw records:", len(df))

    # Keep only valid labels
    df = df[df["Label"].isin([0, 1])]

    # Pivot table → multi-label format
    pivot_df = df.pivot_table(
        index="SMILES",
        columns="Target",
        values="Label",
        aggfunc="max",  # if multiple entries, keep active if any
        fill_value=0
    )

    pivot_df.reset_index(inplace=True)

    print("Final dataset shape:", pivot_df.shape)

    pivot_df.to_csv(OUTPUT_PATH, index=False)
    print("Final dataset saved to:", OUTPUT_PATH)


if __name__ == "__main__":
    build_multilabel_dataset()