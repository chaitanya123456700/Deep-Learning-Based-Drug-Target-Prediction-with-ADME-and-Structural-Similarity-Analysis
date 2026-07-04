import streamlit as st
import pandas as pd
import plotly.express as px

from rdkit import Chem
from rdkit.Chem import Draw

from backend.predictor import predict_targets
from backend.toxicity import predict_toxicity
from backend.synthetic_access import calculate_sa_score
from backend.adme import calculate_adme


def render_dashboard(smiles):

    st.subheader(
        "📊 Molecule Intelligence Dashboard"
    )

    # ---------------------------------
    # BACKEND ANALYSIS
    # ---------------------------------

    predictions = predict_targets(smiles)

    pred_df = pd.DataFrame(predictions)

    pred_df = pred_df.sort_values(
        "Probability",
        ascending=False
    ).head(10)

    top_target = pred_df.iloc[0]["Target"]

    top_prob = pred_df.iloc[0]["Probability"]

    tox = predict_toxicity(smiles)

    sa = calculate_sa_score(smiles)

    adme = calculate_adme(smiles)

    # ---------------------------------
    # TOP METRICS
    # ---------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Top Target",
            top_target
        )

    with col2:

        st.metric(
            "Prediction Confidence",
            round(top_prob, 3)
        )

    with col3:

        st.metric(
            "Safety",
            tox["Overall Toxicity"]
        )

    with col4:

        st.metric(
            "SA Score",
            sa["SA Score"]
        )

    # ---------------------------------
    # MAIN GRID
    # ---------------------------------

    left, right = st.columns([1, 2])

    # ---------------------------------
    # LEFT PANEL
    # ---------------------------------

    with left:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Molecule Structure"
        )

        mol = Chem.MolFromSmiles(smiles)

        if mol:

            img = Draw.MolToImage(
                mol,
                size=(420,420)
            )

            st.image(img)

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # QUICK INSIGHTS
        # -----------------------------

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader("Quick Insights")

        insights = []

        if tox["Overall Toxicity"] == "Safe":

            insights.append(
                "✅ Molecule appears relatively safe."
            )

        else:

            insights.append(
                "⚠ Toxicity concerns detected."
            )

        if adme["Lipinski Rule"] == "Pass":

            insights.append(
                "✅ Lipinski compliant."
            )

        if sa["SA Score"] < 6:

            insights.append(
                "✅ Moderate synthesis feasibility."
            )

        insights.append(
            f"🎯 Highest affinity prediction: {top_target}"
        )

        for item in insights:

            st.write(item)

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # RIGHT PANEL
    # ---------------------------------

    with right:

        # -----------------------------
        # TARGET CHART
        # -----------------------------

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Target Prediction Overview"
        )

        fig = px.bar(

            pred_df,

            x="Target",

            y="Probability",

            color="Class",

            text="Probability"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

        # -----------------------------
        # CLASS DISTRIBUTION
        # -----------------------------

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Target Class Distribution"
        )

        class_df = pred_df.groupby(

            "Class"

        )["Probability"].mean().reset_index()

        pie = px.pie(

            class_df,

            values="Probability",

            names="Class",

            hole=0.4
        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # SUMMARY SECTION
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Integrated Molecular Assessment"
    )

    summary = f"""

    This molecule demonstrates predicted
    activity primarily toward {top_target}.

    Drug-likeness analysis indicates
    {'good' if adme['Lipinski Rule'] == 'Pass' else 'moderate'}
    pharmaceutical compatibility.

    Toxicity assessment suggests the molecule is
    {tox['Overall Toxicity'].lower()}.

    Synthetic accessibility analysis indicates
    {sa['Difficulty'].lower()}
    synthesis complexity.
    """

    st.write(summary)

    st.markdown("</div>", unsafe_allow_html=True)