import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.metrics import (
    ConfusionMatrixDisplay,
    confusion_matrix
)

# =====================================================
# MODEL RESULTS
# =====================================================

results = {

    "FNN": {

        "Accuracy": 0.9850,
        "Precision": 0.7828,
        "Recall": 0.9326,
        "F1 Score": 0.8512,
        "ROC-AUC": 0.9882
    },

    "XGBoost": {

        "Accuracy": 0.9867,
        "Precision": 0.8716,
        "Recall": 0.8317,
        "F1 Score": 0.8512,
        "ROC-AUC": 0.9875
    },

    "GNN": {

        "Accuracy": 0.9480,
        "Precision": 0.3694,
        "Recall": 0.1895,
        "F1 Score": 0.2505,
        "ROC-AUC": 0.7962
    }
}

# =====================================================
# CREATE DATAFRAME
# =====================================================

df = pd.DataFrame(results).T

print("\nMODEL COMPARISON")
print("-------------------------")
print(df)

# =====================================================
# COMPLETE METRIC COMPARISON
# =====================================================

plt.figure(figsize=(12,6))

x = np.arange(len(df.index))

width = 0.15

metrics = df.columns.tolist()

for i, metric in enumerate(metrics):

    plt.bar(

        x + i * width,

        df[metric],

        width,

        label=metric
    )

plt.xticks(

    x + width * 2,

    df.index
)

plt.ylim(0,1.1)

plt.ylabel("Score")

plt.title(
    "Deep Learning and ML Model Comparison"
)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()

# =====================================================
# INDIVIDUAL METRIC PLOTS
# =====================================================

for metric in metrics:

    plt.figure(figsize=(7,5))

    plt.bar(

        df.index,

        df[metric]
    )

    plt.ylim(0,1.1)

    plt.ylabel(metric)

    plt.title(f"{metric} Comparison")

    plt.grid(True)

    plt.tight_layout()

    plt.show()

# =====================================================
# RADAR CHART
# =====================================================

categories = list(df.columns)

N = len(categories)

angles = np.linspace(

    0,
    2 * np.pi,
    N,
    endpoint=False

).tolist()

angles += angles[:1]

fig, ax = plt.subplots(

    figsize=(8,8),

    subplot_kw=dict(polar=True)
)

for model in df.index:

    values = df.loc[model].tolist()

    values += values[:1]

    ax.plot(

        angles,

        values,

        linewidth=2,

        label=model
    )

    ax.fill(

        angles,

        values,

        alpha=0.1
    )

ax.set_xticks(angles[:-1])

ax.set_xticklabels(categories)

ax.set_ylim(0,1)

plt.title(
    "Model Performance Radar Chart"
)

plt.legend(
    loc='upper right'
)

plt.show()

# =====================================================
# BEST MODEL SELECTION
# =====================================================

best_model = df["ROC-AUC"].idxmax()

print("\nBEST MODEL")
print("-------------------------")

print(
    f"Best Performing Model: {best_model}"
)

# =====================================================
# PERFORMANCE SUMMARY TABLE
# =====================================================

plt.figure(figsize=(10,3))

plt.axis('off')

table = plt.table(

    cellText=np.round(df.values,4),

    rowLabels=df.index,

    colLabels=df.columns,

    loc='center'
)

table.auto_set_font_size(False)

table.set_fontsize(10)

table.scale(1.2,1.5)

plt.title(
    "Performance Metrics Table"
)

plt.show()

# =====================================================
# FINAL COMPARISON SCORE
# =====================================================

df["Average Score"] = df.mean(axis=1)

plt.figure(figsize=(7,5))

plt.bar(

    df.index,

    df["Average Score"]
)

plt.ylabel("Average Metric Score")

plt.title(
    "Overall Model Performance"
)

plt.ylim(0,1)

plt.grid(True)

plt.show()