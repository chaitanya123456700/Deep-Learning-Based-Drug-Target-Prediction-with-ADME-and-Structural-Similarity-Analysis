import streamlit as st
import pandas as pd
import plotly.express as px
import requests

from backend.predictor import predict_targets


def search_pubmed(query):

    # ---------------------------------
    # SEARCH IDs
    # ---------------------------------

    search_url = (

        "https://eutils.ncbi.nlm.nih.gov/"
        "entrez/eutils/esearch.fcgi"
    )

    params = {

        "db": "pubmed",

        "term": query,

        "retmode": "json",

        "retmax": 10
    }

    response = requests.get(
        search_url,
        params=params
    )

    data = response.json()

    ids = data["esearchresult"]["idlist"]

    if not ids:

        return []

    # ---------------------------------
    # FETCH DETAILS
    # ---------------------------------

    fetch_url = (

        "https://eutils.ncbi.nlm.nih.gov/"
        "entrez/eutils/esummary.fcgi"
    )

    fetch_params = {

        "db": "pubmed",

        "id": ",".join(ids),

        "retmode": "json"
    }

    fetch_response = requests.get(
        fetch_url,
        params=fetch_params
    )

    details = fetch_response.json()

    papers = []

    for pid in ids:

        item = details["result"].get(pid)

        if item:

            papers.append({

                "Title": item.get("title", ""),

                "Year": item.get("pubdate", "")[:4],

                "Journal": item.get("fulljournalname", ""),

                "Authors": ", ".join([

                    a["name"]

                    for a in item.get("authors", [])
                ]),

                "PubMed":

                f"https://pubmed.ncbi.nlm.nih.gov/{pid}/"
            })

    return papers


def render_literature(smiles):

    st.subheader(
        "📚 Literature Intelligence Workspace"
    )

    # ---------------------------------
    # PREDICT TARGETS
    # ---------------------------------

    predictions = predict_targets(smiles)

    pred_df = pd.DataFrame(predictions)

    pred_df = pred_df.sort_values(
        "Probability",
        ascending=False
    ).head(5)

    targets = pred_df["Target"].tolist()

    # ---------------------------------
    # TARGET SELECTOR
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    target = st.selectbox(

        "Select Biological Target",

        targets
    )

    query = f"{target} drug discovery"

    st.write(
        f"Searching PubMed for: {query}"
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # SEARCH PAPERS
    # ---------------------------------

    papers = search_pubmed(query)

    if not papers:

        st.warning(
            "No literature found."
        )

        return

    # ---------------------------------
    # OVERVIEW METRICS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Papers Retrieved",
            len(papers)
        )

    with col2:

        years = [

            int(p["Year"])

            for p in papers

            if p["Year"].isdigit()
        ]

        latest = max(years) if years else "N/A"

        st.metric(
            "Latest Publication",
            latest
        )

    with col3:

        journals = len(set([
            p["Journal"]
            for p in papers
        ]))

        st.metric(
            "Journals",
            journals
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # TIMELINE CHART
    # ---------------------------------

    years_df = pd.DataFrame({

        "Year": [

            p["Year"]

            for p in papers

            if p["Year"].isdigit()
        ]
    })

    if not years_df.empty:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(
            "Publication Timeline"
        )

        timeline = years_df["Year"].value_counts()

        timeline = timeline.reset_index()

        timeline.columns = [
            "Year",
            "Publications"
        ]

        fig = px.bar(

            timeline,

            x="Year",

            y="Publications",

            color="Publications"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # PAPER CARDS
    # ---------------------------------

    for paper in papers:

        st.markdown("""
        <div class="glass-card">
        """, unsafe_allow_html=True)

        st.subheader(paper["Title"])

        st.write(
            f"📅 Year: {paper['Year']}"
        )

        st.write(
            f"🧪 Journal: {paper['Journal']}"
        )

        st.write(
            f"👨‍🔬 Authors: {paper['Authors']}"
        )

        st.markdown(

            f"[🔗 View on PubMed]"
            f"({paper['PubMed']})"
        )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # INSIGHTS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "Research Insights"
    )

    insights = [

        f"📚 Literature retrieved for {target}.",

        "🧬 Research trends help validate predicted targets.",

        "🔍 Recent publications indicate active scientific interest.",

        "🧪 Literature mining supports biological relevance analysis."
    ]

    for item in insights:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)