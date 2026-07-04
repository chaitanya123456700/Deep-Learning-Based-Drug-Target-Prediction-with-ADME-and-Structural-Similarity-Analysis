import torch
import numpy as np

from backend.fingerprint import smiles_to_fp
from backend.model import DrugTargetModel

# =========================================
# LOAD CHECKPOINT
# =========================================

checkpoint = torch.load(

    "backend/saved_model.pth",

    map_location=torch.device("cpu")
)

targets = checkpoint["targets"]

# =========================================
# LOAD MODEL
# =========================================

model = DrugTargetModel(

    2048,

    len(targets)
)

model.load_state_dict(

    checkpoint["model_state_dict"]
)

model.eval()

# =========================================
# TARGET CLASS MAPPING
# =========================================

def get_target_class(target):

    target_classes = {

        "ABL1": "Kinase",
        "EGFR": "Kinase",
        "VEGFR2": "Kinase",
        "BRAF": "Kinase",
        "JAK2": "Kinase",

        "DRD2": "GPCR",
        "HTR2A": "GPCR",
        "ADRB2": "GPCR",

        "COX2": "Enzyme",
        "ACHE": "Enzyme",
        "MAOA": "Enzyme",

        "HDAC1": "Epigenetic",

        "ESR1": "Nuclear Receptor",
        "AR": "Nuclear Receptor"
    }

    return target_classes.get(
        target,
        "Other"
    )

# =========================================
# PREDICTION FUNCTION
# =========================================

def predict_targets(smiles):

    # -------------------------------------
    # FINGERPRINT
    # -------------------------------------

    fp = smiles_to_fp(smiles)

    if fp is None:

        return None

    # -------------------------------------
    # TO TENSOR
    # -------------------------------------

    tensor = torch.tensor(

        fp,

        dtype=torch.float32
    ).unsqueeze(0)

    # -------------------------------------
    # MODEL INFERENCE
    # -------------------------------------

    with torch.no_grad():

        # -----------------------------
        # RAW LOGITS
        # -----------------------------

        outputs = model(tensor)

        # -----------------------------
        # CONVERT TO PROBABILITIES
        # -----------------------------

        probs = torch.sigmoid(
            outputs
        )

    # -------------------------------------
    # NUMPY
    # -------------------------------------

    probs = probs.numpy().flatten()

    # -------------------------------------
    # CREATE RESULTS
    # -------------------------------------

    results = []

    for t, p in zip(targets, probs):

        results.append({

            "Target": t,

            "Class": get_target_class(t),

            # percentage
            "Probability": round(
                float(p * 100),
                2
            )
        })

    # -------------------------------------
    # SORT
    # -------------------------------------

    results = sorted(

        results,

        key=lambda x:
        x["Probability"],

        reverse=True
    )

    return results