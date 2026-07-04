from rdkit import Chem
from rdkit.Chem import AllChem, DataStructs
import pandas as pd

DATASET_PATH = "backend/data/final_dataset.csv"

def get_fp(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=2048)

def find_similar(smiles, top_n=5):
    query_fp = get_fp(smiles)
    if query_fp is None:
        return []

    df = pd.read_csv(DATASET_PATH)

    results = []

    # limit for speed
    for s in df["SMILES"].head(500):
        fp = get_fp(s)
        if fp:
            sim = DataStructs.TanimotoSimilarity(query_fp, fp)
            results.append((s, sim))

    results.sort(key=lambda x: x[1], reverse=True)

    return results[:top_n]