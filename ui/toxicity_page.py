import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from backend.toxicity import predict_toxicity


def render_toxicity(smiles):

    st.subheader(
        "☠ Toxicity Analysis"
    )

    tox = predict_toxicity(smiles)

    if not tox:

        st.error("Invalid SMILES")

        return

    # ---------------------------------
    # RISK CARDS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader("Toxicity Risks")

    col1, col2, col3 = st.columns(3)

    metrics = [

        ("AMES",
         tox["AMES Toxicity"]),

        ("hERG",
         tox["hERG Toxicity"]),

        ("Hepatotoxicity",
         tox["Hepatotoxicity"])
    ]

    cols = [col1, col2, col3]

    for col, (name, value) in zip(cols, metrics):

        with col:

            if value == "Low Risk":

                st.success(
                    f"{name}\n\nLow Risk"
                )

            else:

                st.error(
                    f"{name}\n\nHigh Risk"
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # MAIN GRID
    # ---------------------------------

    left, right = st.columns([1, 1])

    # ---------------------------------
    # LEFT — PIE CHART
    # ---------------------------------

    with left:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader("Risk Distribution")

        pie_df = pd.DataFrame({

            "Category": [

                "Low Risk",
                "High Risk"
            ],

            "Count": [

                sum([
                    tox["AMES Toxicity"] == "Low Risk",
                    tox["hERG Toxicity"] == "Low Risk",
                    tox["Hepatotoxicity"] == "Low Risk"
                ]),

                sum([
                    tox["AMES Toxicity"] == "High Risk",
                    tox["hERG Toxicity"] == "High Risk",
                    tox["Hepatotoxicity"] == "High Risk"
                ])
            ]
        })

        fig = px.pie(

            pie_df,

            values="Count",

            names="Category",

            hole=0.45
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # RIGHT — SAFETY GAUGE
    # ---------------------------------

    with right:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader("Overall Safety")

        risk_count = sum([

            tox["AMES Toxicity"] == "High Risk",

            tox["hERG Toxicity"] == "High Risk",

            tox["Hepatotoxicity"] == "High Risk"
        ])

        safety_score = 100 - (risk_count * 33)

        gauge = go.Figure(go.Indicator(

            mode="gauge+number",

            value=safety_score,

            title={"text": "Safety Score"},

            gauge={

                "axis": {"range": [0, 100]},

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "red"
                    },

                    {
                        "range": [40, 70],
                        "color": "orange"
                    },

                    {
                        "range": [70, 100],
                        "color": "green"
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
    # INSIGHTS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Toxicity Insights"
    )

    insights = []

    if tox["AMES Toxicity"] == "High Risk":

        insights.append(
            "⚠ Possible mutagenicity risk detected."
        )

    else:

        insights.append(
            "✅ Low mutagenicity probability."
        )

    if tox["hERG Toxicity"] == "High Risk":

        insights.append(
            "⚠ Potential cardiotoxicity concern."
        )

    else:

        insights.append(
            "✅ Low hERG inhibition risk."
        )

    if tox["Hepatotoxicity"] == "High Risk":

        insights.append(
            "⚠ Potential liver toxicity concern."
        )

    else:

        insights.append(
            "✅ Low hepatotoxicity risk."
        )

    for item in insights:

        st.write(item)

    # ---------------------------------
    # OVERALL STATUS
    # ---------------------------------

    st.subheader("Final Assessment")

    if tox["Overall Toxicity"] == "Safe":

        st.success(
            "Molecule appears relatively safe."
        )

    else:

        st.error(
            "Potential toxicity concerns detected."
        )

    st.markdown("</div>", unsafe_allow_html=True)