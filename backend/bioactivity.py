import requests


TARGET_MAP = {

    "EGFR": "epidermal growth factor receptor",

    "VEGFR2": "vascular endothelial growth factor receptor 2",

    "HDAC1": "histone deacetylase 1",

    "HTR2A": "5-hydroxytryptamine receptor 2A",

    "DRD2": "dopamine receptor D2",

    "JAK2": "tyrosine-protein kinase JAK2",

    "BRAF": "B-raf proto-oncogene",

    "COX2": "cyclooxygenase-2",

    "ACHE": "acetylcholinesterase",

    "ESR1": "estrogen receptor"
}


def fetch_bioactivity(target_name, limit=5):

    query = TARGET_MAP.get(target_name, target_name)

    # -----------------------------------
    # Search target directly
    # -----------------------------------
    target_url = (
        "https://www.ebi.ac.uk/chembl/api/data/target/search.json"
        f"?q={query}"
    )

    target_response = requests.get(target_url)

    if target_response.status_code != 200:
        return []

    target_data = target_response.json()

    targets = target_data.get("targets", [])

    if not targets:
        return []

    # Take first matched target
    target_id = targets[0]["target_chembl_id"]

    # -----------------------------------
    # Fetch activities for target
    # -----------------------------------
    activity_url = (
        "https://www.ebi.ac.uk/chembl/api/data/activity.json"
        f"?target_chembl_id={target_id}"
        f"&limit={limit}"
    )

    activity_response = requests.get(activity_url)

    if activity_response.status_code != 200:
        return []

    activity_data = activity_response.json()

    activities = []

    for item in activity_data.get("activities", []):

        activities.append({

            "Target": item.get(
                "target_pref_name",
                query
            ),

            "Molecule": item.get(
                "molecule_chembl_id",
                "N/A"
            ),

            "Type": item.get(
                "standard_type",
                "N/A"
            ),

            "Value": item.get(
                "standard_value",
                "N/A"
            ),

            "Units": item.get(
                "standard_units",
                ""
            )
        })

    return activities