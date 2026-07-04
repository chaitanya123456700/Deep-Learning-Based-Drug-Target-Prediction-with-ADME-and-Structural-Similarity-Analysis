import streamlit as st
import pandas as pd

from backend.predictor import predict_targets
from backend.adme import calculate_adme
from backend.toxicity import predict_toxicity
from backend.synthetic_access import calculate_sa_score

from backend.interpreter import (
    generate_interpretation
)


def render_interpreter(smiles):

    st.subheader(
        "🧠 Unified AI Interpretation Engine"
    )

    # ---------------------------------
    # FETCH MODULE OUTPUTS
    # ---------------------------------

    predictions = predict_targets(smiles)

    pred_df = pd.DataFrame(predictions)

    pred_df = pred_df.sort_values(
        "Probability",
        ascending=False
    )

    top_prediction = pred_df.iloc[0]

    adme = calculate_adme(smiles)

    toxicity = predict_toxicity(smiles)

    sa = calculate_sa_score(smiles)

    # ---------------------------------
    # GENERATE INTERPRETATION
    # ---------------------------------

    result = generate_interpretation(

        top_prediction,
        adme,
        toxicity,
        sa
    )

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
            top_prediction["Target"]
        )

    with col2:

        st.metric(
            "Confidence",
            round(
                top_prediction["Probability"],
                3
            )
        )

    with col3:

        st.metric(
            "Safety",
            toxicity["Overall Toxicity"]
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # SCIENTIFIC INSIGHTS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Scientific Interpretation"
    )

    for item in result["Insights"]:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # FINAL ASSESSMENT
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Integrated Molecular Assessment"
    )

    for item in result["Final Assessment"]:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)