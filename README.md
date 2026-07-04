# 🧬 AI-Powered Multi-Target Drug Discovery Platform

> An end-to-end AI-driven drug discovery platform that predicts biological targets, evaluates drug-likeness, assesses toxicity, analyzes molecular similarity, visualizes 3D structures, retrieves bioactivity information, searches scientific literature, and estimates synthetic accessibility from a single SMILES string.

---

# Overview

Drug discovery is a complex, time-consuming, and expensive process involving multiple stages such as target identification, compound screening, toxicity assessment, pharmacokinetic evaluation, and biological validation.

This platform integrates Artificial Intelligence, Deep Learning, Molecular Informatics, and Cheminformatics into a single interactive system capable of performing multiple computational analyses from a single molecular structure.

The platform accepts a **SMILES representation** of a molecule and performs:

- Multi-target prediction using Deep Learning
- Drug-likeness (ADME) analysis
- Toxicity prediction
- Molecular similarity search
- 3D molecular visualization
- Bioactivity retrieval from ChEMBL
- Literature search from PubMed
- Synthetic accessibility estimation
- AI-generated interpretation of predictions

---

# Features

- Multi-target Drug Target Prediction
- Drug-Likeness (Lipinski Rule of Five)
- ADME Property Calculation
- Toxicity Assessment
- Molecular Similarity Search
- Interactive 3D Molecular Viewer
- Bioactivity Retrieval using ChEMBL API
- Scientific Literature Search using PubMed API
- Synthetic Accessibility Estimation
- AI-Based Interpretation Module
- Comparative Evaluation of Multiple Machine Learning Models

---

# System Architecture

<p align="center">
<img src="images/system_architecture.png" width="900">
</p>

The platform follows a modular architecture consisting of:

```
SMILES Input
      │
      ▼
Fingerprint Generation
(Morgan Fingerprints)
      │
      ▼
Deep Learning Predictor
      │
      ▼
Predicted Targets
      │
 ┌────┼─────────────────────────────────────┐
 ▼    ▼        ▼       ▼       ▼       ▼
ADME Toxicity Similarity Bioactivity Literature
 │
 ▼
Synthetic Accessibility
 │
 ▼
AI Interpretation
```

---

# Dataset Construction

The dataset was automatically collected from the **ChEMBL Database**.

Selected biological targets include:

- EGFR
- ABL1
- BRAF
- VEGFR2
- JAK2
- DRD2
- HTR2A
- ADRB2
- COX2
- ACHE
- HDAC1
- MAOA
- ESR1
- AR

For every target:

- Bioactivity records were downloaded
- IC50 values were extracted
- Molecules with IC50 ≤ 1000 nM were labeled Active
- Remaining compounds were labeled Inactive

The collected data was transformed into a **multi-label classification dataset**, where each molecule may interact with multiple biological targets.

---

# Molecular Representation

Instead of directly feeding SMILES into neural networks, every molecule is converted into a **2048-bit Morgan Fingerprint**.

Morgan Fingerprints encode:

- Atomic neighborhoods
- Bond connectivity
- Circular molecular environments

Advantages:

- Fixed-length representation
- Captures molecular topology
- Efficient for machine learning
- Widely used in cheminformatics

---

# Deep Learning Models Evaluated

Three different machine learning approaches were implemented and compared.

---

## 1. Classical Feed Forward Neural Network

Architecture:

```
2048
 ↓
Linear(1024)
 ↓
BatchNorm
 ↓
ReLU
 ↓
Dropout

 ↓
Linear(512)

 ↓
BatchNorm

 ↓
ReLU

 ↓
Dropout

 ↓
Linear(256)

 ↓
BatchNorm

 ↓
ReLU

 ↓
Dropout

 ↓
Output Layer
```

Features:

- Multi-label Classification
- BCEWithLogitsLoss
- Batch Normalization
- Dropout Regularization
- Early Stopping
- Learning Rate Scheduler
- Threshold Optimization

---

## 2. Graph Neural Network (GCN)

Instead of fingerprints, molecules are represented as graphs.

Nodes:

- Atoms

Edges:

- Chemical Bonds

The model performs message passing between neighboring atoms to learn molecular representations.

Architecture:

```
Molecular Graph

↓

GCN Layer

↓

ReLU

↓

GCN Layer

↓

Graph Pooling

↓

Fully Connected Layers

↓

Predicted Targets
```

Advantages:

- Preserves molecular topology
- Learns atom interactions directly
- Better structural understanding

---

## 3. XGBoost Classifier

Gradient Boosted Decision Trees trained on Morgan Fingerprints.

Advantages:

- Fast training
- High interpretability
- Excellent performance on tabular molecular descriptors
- Robust against overfitting

---

# Model Performance

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---------|----------|-----------|----------|-----------|-----------|
| Feed Forward NN | 98.46% | 77.72% | 93.26% | 84.78% | 98.61% |
| Graph Neural Network | 94.80% | 36.94% | 18.95% | 25.05% | 79.62% |
| XGBoost | 98.67% | 87.16% | 83.17% | 85.12% | 98.75% |

---

# Model Comparison

Insert comparison plots here.

```
images/

accuracy.png

precision.png

recall.png

f1.png

roc_auc.png

comparison_chart.png
```

---

# Training Curves

Insert:

- Training Loss
- Validation Loss
- Early Stopping Plot

---

# User Interface

---

## Dashboard

Displays overall molecular analysis summary.

**Screenshot**

```
images/dashboard.png
```

---

## Target Prediction

Predicts the probability of interaction with multiple biological targets.

Displays:

- Target Name
- Target Class
- Prediction Probability

**Screenshot**

```
images/prediction.png
```

---

## Drug-Likeness

Calculates:

- Molecular Weight
- LogP
- H-Bond Donors
- H-Bond Acceptors
- TPSA
- Rotatable Bonds

Evaluates Lipinski's Rule of Five.

**Screenshot**

```
images/adme.png
```

---

## Similarity Search

Finds structurally similar compounds using:

- Morgan Fingerprints
- Tanimoto Similarity

Displays:

- Similar Molecules
- Similarity Scores

**Screenshot**

```
images/similarity.png
```

---

## Toxicity Prediction

Evaluates toxicity risk using molecular descriptors.

Displays:

- Toxic / Non-toxic Prediction
- Toxicity Probability

**Screenshot**

```
images/toxicity.png
```

---

## 3D Molecular Viewer

Generates an interactive 3D molecular structure.

Supports:

- Ball & Stick
- Surface
- Stick
- Sphere Models

Displays:

- Molecular Geometry
- SAS Surface
- Van der Waals Surface

**Screenshot**

```
images/3dviewer.png
```

---

## Bioactivity Explorer

Retrieves experimentally validated bioactivity records from ChEMBL.

Displays:

- Target
- Molecule
- IC50
- Activity Type

**Screenshot**

```
images/bioactivity.png
```

---

## Literature Search

Automatically searches PubMed using predicted targets.

Displays:

- Research Papers
- Authors
- Abstract Links
- Publication Information

**Screenshot**

```
images/literature.png
```

---

## Synthetic Accessibility

Estimates synthesis complexity.

Produces a Heuristic SA Score ranging from:

- 1 → Easy to synthesize
- 10 → Very difficult to synthesize

Factors considered:

- Molecular complexity
- Ring systems
- Stereochemistry
- Fragment rarity

**Screenshot**

```
images/sa.png
```

---

## AI Interpretation

Provides an AI-generated explanation of the predicted molecule.

Includes:

- Prediction confidence
- Drug-likeness summary
- Toxicity assessment
- Synthetic feasibility
- Overall recommendation

**Screenshot**

```
images/interpreter.png
```

---

# Project Structure

```
AI-Drug-Platform/

├── app.py

├── backend/

│   ├── predictor.py

│   ├── model.py

│   ├── train_model.py

│   ├── fingerprint.py

│   ├── similarity.py

│   ├── toxicity.py

│   ├── bioactivity.py

│   ├── synthetic_access.py

│   ├── adme.py

│   └── ...

├── ui/

│   ├── dashboard.py

│   ├── prediction_page.py

│   ├── toxicity_page.py

│   ├── similarity_page.py

│   ├── bioactivity_page.py

│   ├── literature_page.py

│   ├── synthetic_page.py

│   ├── viewer3d_page.py

│   └── interpreter_page.py

├── models/

├── images/

├── requirements.txt

└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Drug-Platform.git
```

Create virtual environment

```bash
python -m venv venv
```

Activate

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# Technologies Used

- Python
- PyTorch
- PyTorch Geometric
- XGBoost
- RDKit
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Plotly
- ChEMBL API
- PubMed API

---

# Future Improvements

- Transformer-based Molecular Models
- Graph Attention Networks (GAT)
- Molecular Docking Integration
- Protein Structure Prediction
- Explainable AI (SHAP/LIME)
- Generative Drug Design
- Reinforcement Learning for Molecule Optimization
- Cloud Deployment
- Clinical Trial Data Integration

---

# Author

**K. Chaitanya Reddy**

B.Tech Artificial Intelligence & Data Science

AI Research | Drug Discovery | Deep Learning | Bioinformatics

---

# License

This project is intended for educational and research purposes.
