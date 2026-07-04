import streamlit as st

from streamlit_option_menu import option_menu

# -----------------------------
# UI Imports
# -----------------------------
from ui.explainability_page import render_explainability
from ui.interpreter_page import render_interpreter
from ui.synthetic_page import render_synthetic
from ui.literature_page import render_literature
from ui.viewer3d_page import render_3d_viewer
from ui.dashboard import render_dashboard
from ui.prediction_page import render_prediction
from ui.adme_page import render_adme
from ui.similarity_page import render_similarity
from ui.toxicity_page import render_toxicity
from ui.bioactivity_page import render_bioactivity

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Drug Discovery Platform",
    layout="wide"
)

# -----------------------------
# GLOBAL CSS
# -----------------------------

st.markdown("""
<style>

/* -----------------------------
GLOBAL
----------------------------- */

html, body, [class*="css"]  {

    font-family: 'Inter', sans-serif;
}

/* -----------------------------
APP BACKGROUND
----------------------------- */

.stApp {

    background:
    linear-gradient(
        135deg,
        #0B1020 0%,
        #111827 100%
    );

    color: white;
}

/* -----------------------------
REMOVE STREAMLIT HEADER
----------------------------- */

header {

    visibility: hidden;
}

/* -----------------------------
SIDEBAR
----------------------------- */

[data-testid="stSidebar"] {

    background:
    rgba(17, 24, 39, 0.95);

    border-right:
    1px solid rgba(255,255,255,0.06);
}

/* -----------------------------
GLASS CARD
----------------------------- */

.glass-card {

    background:
    rgba(17, 24, 39, 0.72);

    border:
    1px solid rgba(255,255,255,0.08);

    border-radius: 24px;

    padding: 28px;

    margin-bottom: 24px;

    backdrop-filter: blur(18px);

    box-shadow:
    0 8px 32px rgba(0,0,0,0.35);

    transition: 0.3s ease;
}

/* Hover Effect */

.glass-card:hover {

    transform: translateY(-2px);

    border:
    1px solid rgba(0,212,255,0.25);
}

/* -----------------------------
HERO TITLE
----------------------------- */

.big-title {

    font-size: 3.5rem;

    font-weight: 800;

    background:
    linear-gradient(
        90deg,
        #00D4FF,
        #2563EB
    );

    -webkit-background-clip: text;

    -webkit-text-fill-color: transparent;

    margin-bottom: 10px;
}

/* -----------------------------
SUBTITLE
----------------------------- */

.subtitle {

    color: #9CA3AF;

    font-size: 1.15rem;

    line-height: 1.8;
}

/* -----------------------------
BUTTONS
----------------------------- */

.stButton button {

    background:
    linear-gradient(
        90deg,
        #00D4FF,
        #2563EB
    );

    color: white;

    border-radius: 14px;

    border: none;

    font-weight: 700;

    padding: 12px 24px;

    transition: 0.3s ease;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow:
    0 0 20px rgba(0,212,255,0.4);
}

/* -----------------------------
METRICS
----------------------------- */

[data-testid="metric-container"] {

    background:
    rgba(17,24,39,0.72);

    border:
    1px solid rgba(255,255,255,0.06);

    padding: 18px;

    border-radius: 20px;

    box-shadow:
    0 6px 20px rgba(0,0,0,0.25);
}

/* -----------------------------
DATAFRAMES
----------------------------- */

[data-testid="stDataFrame"] {

    border-radius: 18px;

    overflow: hidden;
}

/* -----------------------------
SCROLLBAR
----------------------------- */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-thumb {

    background: #2563EB;

    border-radius: 10px;
}

/* -----------------------------
TEXT AREA
----------------------------- */

textarea {

    border-radius: 18px !important;

    background:
    rgba(17,24,39,0.85) !important;

    color: white !important;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# SIDEBAR
# -----------------------------

with st.sidebar:

    st.markdown("# 🧬 Drug AI")

    selected = option_menu(

        menu_title=None,

        options=[

            "Dashboard",
            "Prediction",
            "Drug-Likeness",
            "Similarity",
            "3D Viewer",
            "Toxicity",
            "Bioactivity",
            "Literature",
            "Synthetic Access",
            # "Explainable AI",
            "AI Interpretation"
            

        ],

        icons=[

            "house",
            "activity",
            "capsule",
            "diagram-3",
            "box",
            "shield-fill",
            "database-fill",
            "book",
            "tools",
            # "cpu",
            "lightbulb"
        ],

        default_index=0
    )

# -----------------------------
# HERO
# -----------------------------

st.markdown("""

<div class="glass-card">

<div class="big-title">
🧬 AI Drug Discovery Platform
</div>

<div class="subtitle">

Advanced computational platform for:

<br><br>

• Multi-target drug prediction  
• Molecular similarity analysis  
• ADME & toxicity assessment  
• Bioactivity intelligence  
• Synthetic accessibility analysis  

</div>

</div>

""", unsafe_allow_html=True)


# -----------------------------
# INPUT
# -----------------------------

st.markdown("""
<div class="glass-card">
""", unsafe_allow_html=True)

st.subheader("Enter Molecule")

smiles = st.text_area(

    "SMILES Input",

    height=120,

    placeholder="Paste molecule SMILES..."
)

if st.button("Analyze Molecule"):

    st.session_state["smiles"] = smiles

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# CHECK INPUT
# -----------------------------

if "smiles" not in st.session_state:

    st.info(
        "Enter a SMILES string to begin analysis."
    )

    st.stop()

smiles = st.session_state["smiles"]

# -----------------------------
# ROUTING
# -----------------------------

if selected == "Dashboard":
    render_dashboard(smiles)

elif selected == "Prediction":
    render_prediction(smiles)

elif selected == "Drug-Likeness":
    render_adme(smiles)

elif selected == "Similarity":
    render_similarity(smiles)

elif selected == "Toxicity":
    render_toxicity(smiles)

elif selected == "Bioactivity":
    render_bioactivity(smiles)
elif selected == "3D Viewer":
    render_3d_viewer(smiles)
elif selected == "Literature":
    render_literature(smiles)
elif selected == "Synthetic Access":
    render_synthetic(smiles)
# elif selected == "Explainable AI":
#     render_explainability(smiles)
elif selected == "AI Interpretation":
    render_interpreter(smiles)