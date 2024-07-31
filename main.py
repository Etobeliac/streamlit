import streamlit as st
from scripts.scrap_ndd import app  # Import direct de la fonction app

# Configuration des pages
st.set_page_config(layout="wide", page_title="Scripts Linkuma")

# Définition des pages
PAGES = {
    "Scrap NDD": app,
}

# Titre principal
st.sidebar.title("Scripts Linkuma")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("Choisissez un script", list(PAGES.keys()))

# Affichage du script sélectionné
page = PAGES[selection]
page()
