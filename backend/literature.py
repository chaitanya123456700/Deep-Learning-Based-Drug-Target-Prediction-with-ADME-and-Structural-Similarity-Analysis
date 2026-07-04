import requests
from xml.etree import ElementTree


def search_pubmed(query, max_results=5):

    # Step 1: Search PubMed IDs
    search_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"esearch.fcgi?db=pubmed&term={query}&retmax={max_results}"
    )

    response = requests.get(search_url)

    if response.status_code != 200:
        return []

    root = ElementTree.fromstring(response.content)

    ids = [id_elem.text for id_elem in root.findall(".//Id")]

    if not ids:
        return []

    # Step 2: Fetch paper details
    ids_string = ",".join(ids)

    fetch_url = (
        "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        f"efetch.fcgi?db=pubmed&id={ids_string}&retmode=xml"
    )

    fetch_response = requests.get(fetch_url)

    if fetch_response.status_code != 200:
        return []

    fetch_root = ElementTree.fromstring(fetch_response.content)

    papers = []

    for article in fetch_root.findall(".//PubmedArticle"):

        title_elem = article.find(".//ArticleTitle")

        abstract_elem = article.find(".//AbstractText")

        pmid_elem = article.find(".//PMID")

        title = title_elem.text if title_elem is not None else "No Title"

        abstract = (
            abstract_elem.text[:300] + "..."
            if abstract_elem is not None and abstract_elem.text
            else "No Abstract"
        )

        pmid = pmid_elem.text if pmid_elem is not None else ""

        paper_link = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"

        papers.append({
            "Title": title,
            "Abstract": abstract,
            "Link": paper_link
        })

    return papers