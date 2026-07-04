import streamlit as st
import pandas as pd
import plotly.express as px

from rdkit import Chem
from rdkit.Chem import Draw

import py3Dmol
from stmol import showmol

from backend.similarity import find_similar
from backend.viewer3d import generate_3d_molecule


def render_similarity(smiles):

    st.subheader(
        "🔍 Molecular Similarity Explorer"
    )

    similar = find_similar(smiles)

    if not similar:

        st.warning(
            "No similar molecules found."
        )

        return

    # ---------------------------------
    # TOP SUMMARY
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    scores = [score for _, score in similar]

    avg_similarity = sum(scores) / len(scores)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Similar Molecules",
            len(similar)
        )

    with col2:

        st.metric(
            "Highest Similarity",
            round(max(scores), 3)
        )

    with col3:

        st.metric(
            "Average Similarity",
            round(avg_similarity, 3)
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # SIMILARITY GRID
    # ---------------------------------

    cols = st.columns(3)

    for idx, (smi, score) in enumerate(similar):

        with cols[idx % 3]:

            st.markdown("""
            <div class="glass-card">
            """, unsafe_allow_html=True)

            # -------------------------
            # Similarity Header
            # -------------------------

            st.subheader(
                f"{round(score * 100, 1)}% Match"
            )

            # -------------------------
            # Similarity Label
            # -------------------------

            if score > 0.8:

                st.success(
                    "Highly Similar"
                )

            elif score > 0.5:

                st.warning(
                    "Moderately Similar"
                )

            else:

                st.info(
                    "Low Similarity"
                )

            # -------------------------
            # Progress Bar
            # -------------------------

            st.progress(float(score))

            # -------------------------
            # 2D Structure
            # -------------------------

            mol = Chem.MolFromSmiles(smi)

            if mol:

                img = Draw.MolToImage(
                    mol,
                    size=(260,260)
                )

                st.image(img)

            # -------------------------
            # Expandable 3D Viewer
            # -------------------------

            with st.expander(
                "🧬 View 3D Structure"
            ):

                mol_block = generate_3d_molecule(smi)

                if mol_block:

                    viewer = py3Dmol.view(

                        width=300,
                        height=300
                    )

                    viewer.addModel(
                        mol_block,
                        "mol"
                    )

                    viewer.setStyle({
                        "stick": {}
                    })

                    viewer.setBackgroundColor(
                        "black"
                    )

                    viewer.zoomTo()

                    showmol(
                        viewer,
                        height=300,
                        width=300
                    )

            # -------------------------
            # Similarity Insights
            # -------------------------

            st.subheader(
                "Insights"
            )

            insights = []

            if score > 0.8:

                insights.append(
                    "✅ Likely to share biological activity."
                )

            elif score > 0.5:

                insights.append(
                    "⚠ Partial scaffold similarity detected."
                )

            else:

                insights.append(
                    "ℹ Weak structural relationship."
                )

            insights.append(
                "🧪 Molecular fingerprint comparison used."
            )

            for item in insights:

                st.write(item)

            st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # SIMILARITY DISTRIBUTION
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Similarity Distribution"
    )

    chart_df = pd.DataFrame({

        "Molecule": [

            f"Mol {i+1}"
            for i in range(len(scores))
        ],

        "Similarity": scores
    })

    fig = px.bar(

        chart_df,

        x="Molecule",

        y="Similarity",

        color="Similarity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)