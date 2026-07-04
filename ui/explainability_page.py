import streamlit as st
import pandas as pd
import plotly.express as px

from rdkit import Chem
from rdkit.Chem import Descriptors

from backend.predictor import predict_targets


def render_explainability(smiles):

    st.subheader(
        "🧠 Explainable AI Workspace"
    )

    # ---------------------------------
    # PREDICTIONS
    # ---------------------------------

    predictions = predict_targets(smiles)

    df = pd.DataFrame(predictions)

    df = df.sort_values(
        "Probability",
        ascending=False
    ).head(10)

    top_target = df.iloc[0]

    # ---------------------------------
    # OVERVIEW
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Top Target",
            top_target["Target"]
        )

    with col2:

        st.metric(
            "Confidence",
            round(
                top_target["Probability"],
                3
            )
        )

    with col3:

        st.metric(
            "Predicted Class",
            top_target["Class"]
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # CONFIDENCE DISTRIBUTION
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Prediction Confidence Distribution"
    )

    fig = px.bar(

        df,

        x="Target",

        y="Probability",

        color="Probability",

        text="Probability"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # CONFIDENCE ANALYSIS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Confidence Interpretation"
    )

    confidence = top_target["Probability"]

    if confidence > 0.8:

        st.success(
            "High-confidence prediction detected."
        )

    elif confidence > 0.5:

        st.warning(
            "Moderate-confidence prediction."
        )

    else:

        st.error(
            "Low-confidence prediction."
        )

    st.write("""

    Prediction confidence reflects the model's
    estimated probability that the molecule
    interacts with the predicted target.

    Higher confidence often indicates stronger
    fingerprint similarity to known ligands.
    """)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # MOLECULAR REASONING
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Molecular Feature Reasoning"
    )

    mol = Chem.MolFromSmiles(smiles)

    mw = Descriptors.MolWt(mol)

    logp = Descriptors.MolLogP(mol)

    aromatic = Descriptors.RingCount(mol)

    hba = Descriptors.NumHAcceptors(mol)

    hbd = Descriptors.NumHDonors(mol)

    reasoning = []

    if aromatic >= 2:

        reasoning.append(
            "🧬 Aromatic ring systems may support receptor binding interactions."
        )

    if logp > 2:

        reasoning.append(
            "⚛ Moderate lipophilicity may improve membrane permeability."
        )

    if hba + hbd > 5:

        reasoning.append(
            "🧪 Hydrogen bonding potential may stabilize target interactions."
        )

    if mw < 500:

        reasoning.append(
            "✅ Molecular size remains within drug-like space."
        )

    reasoning.append(
        "🔍 Morgan fingerprints were used for molecular representation."
    )

    for item in reasoning:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # TARGET CLASS ANALYSIS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Target Class Analysis"
    )

    class_df = df.groupby(

        "Class"

    )["Probability"].mean().reset_index()

    pie = px.pie(

        class_df,

        values="Probability",

        names="Class",

        hole=0.45
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # AI INSIGHTS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "AI Interpretation Insights"
    )

    insights = [

        "🧠 Model predictions are generated using learned molecular fingerprints.",

        "📊 Probability distributions help estimate interaction likelihood.",

        "🧪 Structural descriptors influence biological compatibility.",

        "⚛ Similar molecular scaffolds often share pharmacological behavior.",

        "🔍 Explainability improves interpretability of AI-driven predictions."
    ]

    for item in insights:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)