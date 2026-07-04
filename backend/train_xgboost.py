import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from xgboost import XGBClassifier

from backend.fingerprint import smiles_to_fp

# ======================================
# LOAD DATA
# ======================================

df = pd.read_csv(
    "backend/data/final_dataset.csv"
)

targets = df.columns[1:]

X = []
y = []

for _, row in df.iterrows():

    fp = smiles_to_fp(
        row["SMILES"]
    )

    if fp is not None:

        X.append(fp)

        y.append(
            row[1:].values.astype(int)
        )

X = np.array(X)
y = np.array(y)

# ======================================
# SPLIT
# ======================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42
)

# ======================================
# MODEL
# ======================================

base_model = XGBClassifier(

    n_estimators=200,

    max_depth=8,

    learning_rate=0.05,

    subsample=0.8,

    colsample_bytree=0.8,

    eval_metric='logloss',

    tree_method='hist'
)

model = MultiOutputClassifier(
    base_model
)

# ======================================
# TRAIN
# ======================================

print("\nTraining XGBoost...\n")

model.fit(
    X_train,
    y_train
)

# ======================================
# PREDICT
# ======================================

preds = model.predict(X_test)

probs = np.array([

    est.predict_proba(X_test)[:,1]

    for est in model.estimators_

]).T

# ======================================
# METRICS
# ======================================

accuracy = accuracy_score(

    y_test.flatten(),

    preds.flatten()
)

precision = precision_score(

    y_test.flatten(),

    preds.flatten()
)

recall = recall_score(

    y_test.flatten(),

    preds.flatten()
)

f1 = f1_score(

    y_test.flatten(),

    preds.flatten()
)

roc_auc = roc_auc_score(

    y_test,

    probs,

    average='macro'
)

# ======================================
# PRINT
# ======================================

print("\nXGBOOST EVALUATION")
print("----------------------")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

# ======================================
# SAVE
# ======================================

joblib.dump(

    model,

    "backend/xgboost_model.pkl"
)

print(
    "\nXGBoost model saved!"
)