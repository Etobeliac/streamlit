import streamlit as st
from scripts import scrap_ndd

Configuration des pages
PAGES = {
    "scrap ndd": scrap_ndd,
}

Titre principal
st.sidebar.title("Scripts Linkuma")

Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("", list(PAGES.keys()), index=0)

Affichage du script sélectionné
page = PAGES[selection]
page.app()
