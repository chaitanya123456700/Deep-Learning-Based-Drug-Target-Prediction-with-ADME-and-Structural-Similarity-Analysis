from rdkit import Chem
from rdkit.Chem import Descriptors


def calculate_sa_score(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    mw = Descriptors.MolWt(mol)

    rings = Descriptors.RingCount(mol)

    rotatable = Descriptors.NumRotatableBonds(mol)

    aromaticity = Descriptors.FractionCSP3(mol)

    h_donors = Descriptors.NumHDonors(mol)

    h_acceptors = Descriptors.NumHAcceptors(mol)

    # ---------------------------------
    # Heuristic SA Score
    # ---------------------------------

    score = (
        (mw / 100)
        + rings
        + rotatable * 0.5
        + (1 - aromaticity) * 2
    )

    score = max(1, min(score, 10))

    # Difficulty
    if score <= 3:
        difficulty = "Easy"

    elif score <= 6:
        difficulty = "Moderate"

    else:
        difficulty = "Difficult"

    return {

        "SA Score": round(score, 2),

        "Difficulty": difficulty,

        "Molecular Weight": round(mw, 2),

        "Ring Count": rings,

        "Rotatable Bonds": rotatable,

        "Fraction CSP3": round(aromaticity, 2),

        "H-Bond Donors": h_donors,

        "H-Bond Acceptors": h_acceptors
    }