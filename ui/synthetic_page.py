import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from rdkit import Chem
from rdkit.Chem import Descriptors

from backend.synthetic_access import calculate_sa_score


def render_synthetic(smiles):

    st.subheader(
        "⚗ Synthetic Accessibility Workspace"
    )

    sa = calculate_sa_score(smiles)

    if not sa:

        st.error("Invalid SMILES")

        return

    # ---------------------------------
    # MOLECULE
    # ---------------------------------

    mol = Chem.MolFromSmiles(smiles)

    # ---------------------------------
    # TOP METRICS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "SA Score",
            sa["SA Score"]
        )

    with col2:

        st.metric(
            "Difficulty",
            sa["Difficulty"]
        )

    with col3:

        ring_count = Descriptors.RingCount(mol)

        st.metric(
            "Ring Systems",
            ring_count
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # MAIN GRID
    # ---------------------------------

    left, right = st.columns([1, 1])

    # ---------------------------------
    # LEFT — GAUGE
    # ---------------------------------

    with left:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Synthesis Complexity"
        )

        gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=sa["SA Score"],

            title={
                "text": "SA Score"
            },

            gauge={

                "axis": {
                    "range": [1, 10]
                },

                "steps": [

                    {
                        "range": [1, 4],
                        "color": "green"
                    },

                    {
                        "range": [4, 7],
                        "color": "orange"
                    },

                    {
                        "range": [7, 10],
                        "color": "red"
                    }
                ]
            }
        ))

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # RIGHT — ANALYTICS
    # ---------------------------------

    with right:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Structural Analytics"
        )

        analytics_df = pd.DataFrame({

            "Metric": [

                "Molecular Weight",
                "Ring Count",
                "Rotatable Bonds",
                "Fraction CSP3",
                "H-Bond Donors",
                "H-Bond Acceptors"
            ],

            "Value": [

                round(
                    Descriptors.MolWt(mol),
                    2
                ),

                Descriptors.RingCount(mol),

                Descriptors.NumRotatableBonds(mol),

                round(
                    Descriptors.FractionCSP3(mol),
                    2
                ),

                Descriptors.NumHDonors(mol),

                Descriptors.NumHAcceptors(mol)
            ]
        })

        st.dataframe(
            analytics_df,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # COMPLEXITY PROFILE
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Complexity Profile"
    )

    complexity_df = pd.DataFrame({

        "Feature": [

            "Ring Complexity",
            "Flexibility",
            "Polarity",
            "3D Character"
        ],

        "Value": [

            Descriptors.RingCount(mol),

            Descriptors.NumRotatableBonds(mol),

            Descriptors.TPSA(mol) / 20,

            Descriptors.FractionCSP3(mol) * 10
        ]
    })

    fig = px.bar(

        complexity_df,

        x="Feature",

        y="Value",

        color="Value"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # MEDICINAL INSIGHTS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Medicinal Chemistry Insights"
    )

    insights = []

    if sa["SA Score"] < 4:

        insights.append(
            "✅ Molecule likely easy to synthesize."
        )

    elif sa["SA Score"] < 7:

        insights.append(
            "⚠ Moderate synthetic complexity."
        )

    else:

        insights.append(
            "❌ Challenging synthesis expected."
        )

    if Descriptors.RingCount(mol) > 3:

        insights.append(
            "⚠ Multiple ring systems increase synthetic difficulty."
        )

    if Descriptors.NumRotatableBonds(mol) > 10:

        insights.append(
            "⚠ High flexibility may complicate optimization."
        )

    if Descriptors.FractionCSP3(mol) > 0.5:

        insights.append(
            "✅ Good 3D complexity observed."
        )

    insights.append(
        "🧪 Synthetic accessibility estimated using molecular complexity heuristics."
    )

    for item in insights:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)