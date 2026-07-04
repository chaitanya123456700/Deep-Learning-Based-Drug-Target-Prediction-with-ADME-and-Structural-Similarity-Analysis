import torch
import torch.nn as nn
import torch.nn.functional as F

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from rdkit import Chem

from sklearn.model_selection import train_test_split

from sklearn.metrics import (

    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score
)

from torch_geometric.data import Data
from torch_geometric.loader import DataLoader
from torch_geometric.nn import GCNConv
from torch_geometric.nn import global_mean_pool

# =========================================
# LOAD DATASET
# =========================================

df = pd.read_csv(
    "backend/data/final_dataset.csv"
)

targets = df.columns[1:]

# =========================================
# ATOM FEATURES
# =========================================

def atom_features(atom):

    return [

        atom.GetAtomicNum(),

        atom.GetDegree(),

        atom.GetFormalCharge(),

        atom.GetHybridization().real,

        atom.GetIsAromatic()
    ]

# =========================================
# SMILES → GRAPH
# =========================================

def smiles_to_graph(smiles, label):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    # -------------------------------------
    # NODE FEATURES
    # -------------------------------------

    x = []

    for atom in mol.GetAtoms():

        x.append(
            atom_features(atom)
        )

    x = torch.tensor(
        x,
        dtype=torch.float
    )

    # -------------------------------------
    # EDGES
    # -------------------------------------

    edge_index = []

    for bond in mol.GetBonds():

        i = bond.GetBeginAtomIdx()
        j = bond.GetEndAtomIdx()

        edge_index.append([i, j])
        edge_index.append([j, i])

    edge_index = torch.tensor(
        edge_index,
        dtype=torch.long
    ).t().contiguous()

    # -------------------------------------
    # LABEL
    # -------------------------------------

    y = torch.tensor(
        [label],
        dtype=torch.float
    )

    return Data(

        x=x,

        edge_index=edge_index,

        y=y
    )

# =========================================
# CREATE GRAPH DATASET
# =========================================

graphs = []

for _, row in df.iterrows():

    graph = smiles_to_graph(

        row["SMILES"],

        row[1:].values.astype(float)
    )

    if graph is not None:

        graphs.append(graph)

print(
    f"Total Graphs: {len(graphs)}"
)

# =========================================
# TRAIN / TEST SPLIT
# =========================================

train_graphs, test_graphs = train_test_split(

    graphs,

    test_size=0.2,

    random_state=42
)

train_loader = DataLoader(

    train_graphs,

    batch_size=32,

    shuffle=True
)

test_loader = DataLoader(

    test_graphs,

    batch_size=32
)

# =========================================
# GNN MODEL
# =========================================

class GNNModel(nn.Module):

    def __init__(

        self,

        num_features,

        num_targets
    ):

        super().__init__()

        self.conv1 = GCNConv(

            num_features,

            128
        )

        self.conv2 = GCNConv(

            128,

            64
        )

        self.fc1 = nn.Linear(

            64,

            128
        )

        self.dropout = nn.Dropout(0.3)

        self.fc2 = nn.Linear(

            128,

            num_targets
        )

    def forward(self, data):

        x = data.x
        edge_index = data.edge_index
        batch = data.batch

        # ---------------------------------
        # GRAPH CONVOLUTION
        # ---------------------------------

        x = self.conv1(

            x,

            edge_index
        )

        x = F.relu(x)

        x = self.conv2(

            x,

            edge_index
        )

        x = F.relu(x)

        # ---------------------------------
        # GRAPH POOLING
        # ---------------------------------

        x = global_mean_pool(

            x,

            batch
        )

        # ---------------------------------
        # DENSE LAYERS
        # ---------------------------------

        x = self.fc1(x)

        x = F.relu(x)

        x = self.dropout(x)

        x = self.fc2(x)

        return x

# =========================================
# MODEL INIT
# =========================================

device = torch.device(

    "cuda"

    if torch.cuda.is_available()

    else "cpu"
)

model = GNNModel(

    num_features=5,

    num_targets=len(targets)

).to(device)

# =========================================
# LOSS + OPTIMIZER
# =========================================

criterion = nn.BCEWithLogitsLoss()

optimizer = torch.optim.Adam(

    model.parameters(),

    lr=0.001
)

# =========================================
# TRAINING
# =========================================

epochs = 30

train_losses = []

for epoch in range(epochs):

    model.train()

    total_loss = 0

    for batch in train_loader:

        batch = batch.to(device)

        optimizer.zero_grad()

        outputs = model(batch)

        loss = criterion(

            outputs,

            batch.y
        )

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(train_loader)

    train_losses.append(avg_loss)

    print(

        f"Epoch {epoch+1}/{epochs}"

        f" | Loss: {avg_loss:.4f}"
    )

# =========================================
# EVALUATION
# =========================================

model.eval()

all_probs = []
all_true = []

with torch.no_grad():

    for batch in test_loader:

        batch = batch.to(device)

        outputs = model(batch)

        probs = torch.sigmoid(outputs)

        all_probs.append(

            probs.cpu().numpy()
        )

        all_true.append(

            batch.y.cpu().numpy()
        )

probs = np.vstack(all_probs)
true = np.vstack(all_true)

# =========================================
# THRESHOLD
# =========================================

threshold = 0.2

preds = (
    probs > threshold
).astype(int)

# =========================================
# METRICS
# =========================================

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

# =========================================
# PRINT RESULTS
# =========================================

print("\nGNN EVALUATION")
print("----------------------")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

# =========================================
# LOSS CURVE
# =========================================

plt.figure(figsize=(8,5))

plt.plot(

    train_losses,

    label="Training Loss"
)

plt.xlabel("Epoch")

plt.ylabel("Loss")

plt.title("GNN Training Loss")

plt.legend()

plt.show()

# =========================================
# SAVE MODEL
# =========================================

torch.save({

    "model_state_dict":
    model.state_dict(),

    "targets":
    list(targets)

}, "backend/gnn_model.pth")

print(
    "\nGNN model saved!"
)