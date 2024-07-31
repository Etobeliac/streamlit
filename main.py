import streamlit as st
from scripts import scrap_ndd  # Assurez-vous que ce chemin est correct et que le module existe

# Configuration des pages
st.set_page_config(layout="wide", page_title="Scripts Linkuma")

# Définition des pages
PAGES = {
    "Scrap NDD": scrap_ndd,
}

# Titre principal
st.sidebar.title("Scripts Linkuma")

# Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("Choisissez un script", list(PAGES.keys()))

# Affichage du script sélectionné
page = PAGES[selection]
if hasattr(page, 'app'):
    page.app()
else:
    st.error("La fonction 'app' n'existe pas dans le module sélectionné.")
