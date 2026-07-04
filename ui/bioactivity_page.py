import streamlit as st
import pandas as pd
import plotly.express as px

from backend.predictor import predict_targets
from backend.bioactivity import fetch_bioactivity


def render_bioactivity(smiles):

    st.subheader(
        "🧪 Bioactivity Intelligence"
    )

    # ---------------------------------
    # PREDICT TARGETS
    # ---------------------------------

    predictions = predict_targets(smiles)

    pred_df = pd.DataFrame(predictions)

    pred_df = pred_df.sort_values(
        "Probability",
        ascending=False
    )

    # ---------------------------------
    # THRESHOLD
    # ---------------------------------

    threshold = st.slider(

        "Prediction Threshold",

        0.0,
        1.0,
        0.05
    )

    filtered_df = pred_df[
        pred_df["Probability"] > threshold
    ]

    targets = filtered_df["Target"].tolist()

    if not targets:

        st.warning(
            "No predicted targets above threshold."
        )

        return

    # ---------------------------------
    # OVERVIEW
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader("Bioactivity Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Predicted Targets",
            len(targets)
        )

    with col2:

        st.metric(
            "Highest Confidence",
            round(
                filtered_df.iloc[0]["Probability"],
                3
            )
        )

    with col3:

        st.metric(
            "Threshold",
            threshold
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # TARGET ANALYSIS
    # ---------------------------------

    for target in targets:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(f"🎯 {target}")

        activities = fetch_bioactivity(target)

        if activities:

            activity_df = pd.DataFrame(
                activities
            )

            # -------------------------
            # ACTIVITY TABLE
            # -------------------------

            st.dataframe(
                activity_df,
                use_container_width=True
            )

            # -------------------------
            # NUMERIC FILTER
            # -------------------------

            numeric_df = activity_df.copy()

            numeric_df["Value"] = pd.to_numeric(
                numeric_df["Value"],
                errors="coerce"
            )

            numeric_df = numeric_df.dropna()

            # -------------------------
            # ACTIVITY CHART
            # -------------------------

            if not numeric_df.empty:

                st.subheader(
                    "Activity Distribution"
                )

                fig = px.bar(

                    numeric_df,

                    x="Molecule",

                    y="Value",

                    color="Type",

                    hover_data=["Units"]
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

                # ---------------------
                # SUMMARY STATS
                # ---------------------

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Assays",
                        len(numeric_df)
                    )

                with col2:

                    st.metric(
                        "Best Activity",
                        round(
                            numeric_df["Value"].min(),
                            2
                        )
                    )

                with col3:

                    st.metric(
                        "Average Activity",
                        round(
                            numeric_df["Value"].mean(),
                            2
                        )
                    )

            # -------------------------
            # INSIGHTS
            # -------------------------

            st.subheader(
                "Experimental Insights"
            )

            insights = []

            if len(activity_df) > 3:

                insights.append(
                    "✅ Multiple experimental assay records available."
                )

            if not numeric_df.empty:

                best = numeric_df["Value"].min()

                if best < 100:

                    insights.append(
                        "🔥 Strong bioactivity detected."
                    )

                elif best < 1000:

                    insights.append(
                        "⚠ Moderate bioactivity observed."
                    )

                else:

                    insights.append(
                        "ℹ Weak experimental activity."
                    )

            insights.append(
                "🧪 Data retrieved from ChEMBL."
            )

            for item in insights:

                st.write(item)

        else:

            st.warning(
                f"No ChEMBL activity records for {target}"
            )

        st.markdown("</div>", unsafe_allow_html=True)