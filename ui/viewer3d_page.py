import streamlit as st
import py3Dmol

from stmol import showmol

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors


def generate_3d_molecule(smiles):

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        return None

    mol = Chem.AddHs(mol)

    AllChem.EmbedMolecule(mol)

    AllChem.MMFFOptimizeMolecule(mol)

    mol_block = Chem.MolToMolBlock(mol)

    return mol_block


def render_3d_viewer(smiles):

    st.subheader(
        "🧬 Advanced 3D Molecular Workspace"
    )

    mol_block = generate_3d_molecule(smiles)

    if mol_block is None:

        st.error("Invalid SMILES")

        return

    # ---------------------------------
    # SETTINGS PANEL
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader("Visualization Settings")

    col1, col2, col3 = st.columns(3)

    with col1:

        style = st.selectbox(

            "Render Style",

            [
                "stick",
                "sphere",
                "line",
                "cartoon"
            ]
        )

    with col2:

        bg_color = st.selectbox(

            "Background",

            [
                "black",
                "white",
                "gray"
            ]
        )

    with col3:

        surface = st.selectbox(

            "Surface",

            [
                "None",
                "VDW",
                "SAS"
            ]
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # 3D VIEWER
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    viewer = py3Dmol.view(

        width=900,
        height=600
    )

    viewer.addModel(
        mol_block,
        "mol"
    )

    viewer.setStyle({

        style: {}
    })

    # ---------------------------------
    # SURFACE OPTIONS
    # ---------------------------------

    if surface == "VDW":

        viewer.addSurface(
            py3Dmol.VDW,
            {'opacity': 0.6}
        )

    elif surface == "SAS":

        viewer.addSurface(
            py3Dmol.SAS,
            {'opacity': 0.6}
        )

    # ---------------------------------
    # BACKGROUND
    # ---------------------------------

    viewer.setBackgroundColor(bg_color)

    viewer.zoomTo()

    showmol(
        viewer,
        height=600,
        width=900
    )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # MOLECULAR ANALYTICS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader("Molecular Analytics")

    mol = Chem.MolFromSmiles(smiles)

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Molecular Weight",
            round(
                Descriptors.MolWt(mol),
                2
            )
        )

    with col2:

        st.metric(
            "LogP",
            round(
                Descriptors.MolLogP(mol),
                2
            )
        )

    with col3:

        st.metric(
            "TPSA",
            round(
                Descriptors.TPSA(mol),
                2
            )
        )

    with col4:

        st.metric(
            "Rotatable Bonds",
            Descriptors.NumRotatableBonds(mol)
        )

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------------------------
    # INSIGHTS
    # ---------------------------------

    st.markdown("""
    <div class="glass-card">
    """, unsafe_allow_html=True)

    st.subheader(
        "3D Structural Insights"
    )

    insights = [

        "🧬 3D conformer generated using RDKit embedding.",

        "🧪 MMFF optimization applied for geometry refinement.",

        "🔍 Surface rendering helps visualize steric accessibility.",

        "⚛ Molecular shape influences target binding affinity.",

        "📐 Rotatable bonds impact conformational flexibility."
    ]

    for item in insights:

        st.write(item)

    st.markdown("</div>", unsafe_allow_html=True)