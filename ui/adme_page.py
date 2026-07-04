import streamlit as st
import pandas as pd
import plotly.express as px

from backend.adme import calculate_adme


def render_adme(smiles):

    st.subheader(
        "🧪 Drug-Likeness & ADME"
    )

    adme = calculate_adme(smiles)

    if not adme:

        st.error("Invalid SMILES")

        return

    # ---------------------------------
    # RULE CARDS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader("Drug-Likeness Rules")

    col1, col2, col3, col4 = st.columns(4)

    rules = [

        ("Lipinski", adme["Lipinski Rule"]),

        ("Veber", adme["Veber Rule"]),

        ("Pfizer", adme["Pfizer Rule"]),

        ("Ghose", adme["Ghose Rule"])
    ]

    cols = [col1, col2, col3, col4]

    for col, (rule, status) in zip(cols, rules):

        with col:

            if status == "Pass":

                st.success(
                    f"{rule}\n\nPASS"
                )

            else:

                st.error(
                    f"{rule}\n\nFAIL"
                )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # MAIN GRID
    # ---------------------------------

    left, right = st.columns([1, 1])

    # ---------------------------------
    # LEFT
    # ---------------------------------

    with left:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Molecular Properties"
        )

        prop_df = pd.DataFrame([

            ["Molecular Weight",
             adme["Molecular Weight"]],

            ["LogP",
             adme["LogP"]],

            ["TPSA",
             adme["TPSA"]],

            ["H-Bond Donors",
             adme["H-Bond Donors"]],

            ["H-Bond Acceptors",
             adme["H-Bond Acceptors"]],

            ["Rotatable Bonds",
             adme["Rotatable Bonds"]]

        ], columns=["Property", "Value"])

        st.dataframe(
            prop_df,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # RIGHT
    # ---------------------------------

    with right:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Bioavailability Radar"
        )

        radar_df = pd.DataFrame({

            "Metric": [

                "Lipophilicity",
                "Size",
                "Polarity",
                "Flexibility",
                "HBA",
                "HBD"
            ],

            "Value": [

                adme["LogP"],

                adme["Molecular Weight"] / 100,

                adme["TPSA"] / 20,

                adme["Rotatable Bonds"],

                adme["H-Bond Acceptors"],

                adme["H-Bond Donors"]
            ]
        })

        radar_fig = px.line_polar(

            radar_df,

            r="Value",

            theta="Metric",

            line_close=True
        )

        radar_fig.update_traces(
            fill='toself'
        )

        st.plotly_chart(
            radar_fig,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # DRUG SCORE
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Overall Drug-Likeness"
    )

    pass_count = sum([

        adme["Lipinski Rule"] == "Pass",

        adme["Veber Rule"] == "Pass",

        adme["Pfizer Rule"] == "Pass",

        adme["Ghose Rule"] == "Pass"

    ])

    score = (pass_count / 4) * 100

    st.metric(
        "Drug-Likeness Score",
        f"{score:.0f}%"
    )

    # ---------------------------------
    # INSIGHTS
    # ---------------------------------

    st.subheader(
        "Medicinal Chemistry Insights"
    )

    insights = []

    if adme["LogP"] < 5:

        insights.append(
            "✅ Acceptable lipophilicity"
        )

    if adme["TPSA"] < 140:

        insights.append(
            "✅ Good oral bioavailability expected"
        )

    if adme["Molecular Weight"] < 500:

        insights.append(
            "✅ Molecular size within drug-like range"
        )

    if adme["Rotatable Bonds"] > 10:

        insights.append(
            "⚠ High flexibility may reduce stability"
        )

    for insight in insights:

        st.write(insight)

    st.markdown("</div>", unsafe_allow_html=True)