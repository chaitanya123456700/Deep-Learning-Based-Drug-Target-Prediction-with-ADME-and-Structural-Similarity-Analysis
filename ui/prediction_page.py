import streamlit as st
import pandas as pd
import plotly.express as px

from rdkit import Chem
from rdkit.Chem import Draw

from backend.predictor import predict_targets


def render_prediction(smiles):

    st.subheader("🎯 Target Prediction")

    results = predict_targets(smiles)

    df = pd.DataFrame(results)

    df = df.sort_values(
        "Probability",
        ascending=False
    ).head(10)

    left, right = st.columns([1, 2])

    # -------------------------
    # Molecule
    # -------------------------

    with left:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        mol = Chem.MolFromSmiles(smiles)

        if mol:

            img = Draw.MolToImage(
                mol,
                size=(420,420)
            )

            st.image(img)

        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------
    # Predictions
    # -------------------------

    with right:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.dataframe(
            df,
            use_container_width=True
        )

        fig = px.bar(

            df,

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