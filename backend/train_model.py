import torch
import torch.nn as nn
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from backend.fingerprint import smiles_to_fp

# ===================================
# LOAD DATASET
# ===================================

df = pd.read_csv(
    "backend/data/final_dataset.csv"
)

targets = df.columns[1:]

X = []
y = []

# ===================================
# FINGERPRINT GENERATION
# ===================================

for _, row in df.iterrows():

    fp = smiles_to_fp(row["SMILES"])

    if fp is not None:

        X.append(fp)

        y.append(
            row[1:].values.astype(float)
        )

X = np.array(X)
y = np.array(y)

# ===================================
# TRAIN / VAL / TEST SPLIT
# ===================================

X_train, X_temp, y_train, y_temp = (

    train_test_split(

        X,
        y,

        test_size=0.3,

        random_state=42
    )
)

X_val, X_test, y_val, y_test = (

    train_test_split(

        X_temp,
        y_temp,

        test_size=0.5,

        random_state=42
    )
)

# ===================================
# CONVERT TO TENSORS
# ===================================

X_train = torch.tensor(
    X_train,
    dtype=torch.float32
)

y_train = torch.tensor(
    y_train,
    dtype=torch.float32
)

X_val = torch.tensor(
    X_val,
    dtype=torch.float32
)

y_val = torch.tensor(
    y_val,
    dtype=torch.float32
)

X_test = torch.tensor(
    X_test,
    dtype=torch.float32
)

y_test = torch.tensor(
    y_test,
    dtype=torch.float32
)

# ===================================
# MODEL
# ===================================

from backend.model import DrugTargetModel

# ===================================
# MODEL INIT
# ===================================

model = DrugTargetModel(
    2048,
    len(targets)
)

# ===================================
# CLASS WEIGHTS
# ===================================

positive_counts = y.sum(axis=0)

negative_counts = len(y) - positive_counts

pos_weights = negative_counts / (
    positive_counts + 1e-5
)

pos_weights = torch.tensor(
    pos_weights,
    dtype=torch.float32
)

# ===================================
# LOSS + OPTIMIZER
# ===================================

criterion = nn.BCEWithLogitsLoss(
    pos_weight=pos_weights
)

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=0.001
)

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(

    optimizer,

    mode='min',

    factor=0.5,

    patience=3
)

# ===================================
# EARLY STOPPING
# ===================================

best_val_loss = float('inf')

patience = 5

counter = 0

# ===================================
# TRAINING
# ===================================

epochs = 50

train_losses = []
val_losses = []

for epoch in range(epochs):

    # -----------------------------
    # TRAIN
    # -----------------------------

    model.train()

    optimizer.zero_grad()

    outputs = model(X_train)

    loss = criterion(
        outputs,
        y_train
    )

    loss.backward()

    optimizer.step()

    train_losses.append(
        loss.item()
    )

    # -----------------------------
    # VALIDATION
    # -----------------------------

    model.eval()

    with torch.no_grad():

        val_outputs = model(X_val)

        val_loss = criterion(

            val_outputs,

            y_val
        )

    val_losses.append(
        val_loss.item()
    )

    # -----------------------------
    # LR SCHEDULER
    # -----------------------------

    scheduler.step(
        val_loss.item()
    )

    # -----------------------------
    # EARLY STOPPING
    # -----------------------------

    if val_loss < best_val_loss:

        best_val_loss = val_loss

        counter = 0

        torch.save({

            "model_state_dict":
            model.state_dict(),

            "targets":
            list(targets)

        }, "backend/best_model.pth")

    else:

        counter += 1

    if counter >= patience:

        print("\nEarly stopping triggered")

        break

    # -----------------------------
    # PRINT
    # -----------------------------

    print(

        f"Epoch {epoch+1}/{epochs}"

        f" | Train Loss: {loss.item():.4f}"

        f" | Val Loss: {val_loss.item():.4f}"
    )

# ===================================
# LOAD BEST MODEL
# ===================================

checkpoint = torch.load(
    "backend/best_model.pth"
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

# ===================================
# TEST EVALUATION
# ===================================

model.eval()

with torch.no_grad():

    outputs = model(X_test)

    probs = torch.sigmoid(
        outputs
    ).numpy()

true = y_test.numpy()

# ===================================
# THRESHOLD TUNING
# ===================================

thresholds = np.arange(
    0.05,
    0.5,
    0.05
)

best_threshold = 0
best_f1 = 0

for t in thresholds:

    preds = (
        probs > t
    ).astype(int)

    score = f1_score(

        true.flatten(),

        preds.flatten()
    )

    print(
        f"Threshold {t:.2f}"
        f" → F1 {score:.4f}"
    )

    if score > best_f1:

        best_f1 = score

        best_threshold = t

print(
    f"\nBest Threshold: {best_threshold:.2f}"
)

# ===================================
# FINAL PREDICTIONS
# ===================================

preds = (
    probs > best_threshold
).astype(int)

# ===================================
# METRICS
# ===================================

accuracy = accuracy_score(

    true.flatten(),

    preds.flatten()
)

precision = precision_score(

    true.flatten(),

    preds.flatten()
)

recall = recall_score(

    true.flatten(),

    preds.flatten()
)

f1 = f1_score(

    true.flatten(),

    preds.flatten()
)

roc_auc = roc_auc_score(

    true,

    probs,

    average='macro'
)

# ===================================
# PRINT METRICS
# ===================================

print("\nMODEL EVALUATION")
print("----------------------")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

# ===================================
# LOSS CURVE
# ===================================

plt.figure(figsize=(8,5))

plt.plot(
    train_losses,
    label="Train Loss"
)

plt.plot(
    val_losses,
    label="Validation Loss"
)

plt.xlabel("Epoch")
plt.ylabel("Loss")

plt.title(
    "Training vs Validation Loss"
)

plt.legend()

plt.show()

# ===================================
# SAVE FINAL MODEL
# ===================================

torch.save({

    "model_state_dict":
    model.state_dict(),

    "targets":
    list(targets)

}, "backend/saved_model.pth")

print(
    "\nModel saved successfully!"
)