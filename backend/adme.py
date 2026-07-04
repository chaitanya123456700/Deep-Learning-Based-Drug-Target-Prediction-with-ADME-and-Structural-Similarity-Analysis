from rdkit import Chem
from rdkit.Chem import Descriptors


def calculate_adme(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    mw = Descriptors.MolWt(mol)
    logp = Descriptors.MolLogP(mol)
    h_donors = Descriptors.NumHDonors(mol)
    h_acceptors = Descriptors.NumHAcceptors(mol)
    tpsa = Descriptors.TPSA(mol)
    rotatable = Descriptors.NumRotatableBonds(mol)

    # -------------------------
    # Lipinski Rule
    # -------------------------
    lipinski = (
        mw <= 500 and
        logp <= 5 and
        h_donors <= 5 and
        h_acceptors <= 10
    )

    # -------------------------
    # Veber Rule
    # -------------------------
    veber = (
        rotatable <= 10 and
        tpsa <= 140
    )

    # -------------------------
    # Pfizer Rule
    # -------------------------
    pfizer = not (
        logp > 3 and
        tpsa < 75
    )

    # -------------------------
    # Ghose Rule
    # -------------------------
    ghose = (
        160 <= mw <= 480 and
        -0.4 <= logp <= 5.6
    )

    return {

        "Molecular Weight": round(mw, 2),
        "LogP": round(logp, 2),
        "TPSA": round(tpsa, 2),

        "H-Bond Donors": h_donors,
        "H-Bond Acceptors": h_acceptors,
        "Rotatable Bonds": rotatable,

        "Lipinski Rule": "Pass" if lipinski else "Fail",
        "Veber Rule": "Pass" if veber else "Fail",
        "Pfizer Rule": "Pass" if pfizer else "Fail",
        "Ghose Rule": "Pass" if ghose else "Fail"
    }