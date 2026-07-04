from rdkit import Chem
from rdkit.Chem import Descriptors


def predict_toxicity(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    logp = Descriptors.MolLogP(mol)

    mw = Descriptors.MolWt(mol)

    aromatic_rings = Descriptors.RingCount(mol)

    # ------------------------
    # Heuristic logic
    # ------------------------

    ames = (
        "High Risk"
        if aromatic_rings >= 3
        else "Low Risk"
    )

    herg = (
        "High Risk"
        if logp > 3.5
        else "Low Risk"
    )

    hepatotoxicity = (
        "High Risk"
        if mw > 500
        else "Low Risk"
    )

    overall = (

        "Toxic"

        if (
            ames == "High Risk"
            or herg == "High Risk"
            or hepatotoxicity == "High Risk"
        )

        else "Safe"
    )

    return {

        "AMES Toxicity": ames,

        "hERG Toxicity": herg,

        "Hepatotoxicity": hepatotoxicity,

        "Overall Toxicity": overall
    }