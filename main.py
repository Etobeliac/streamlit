import streamlit as st
from scripts import "nom_du_script"

Configuration des pages
PAGES = {
    "Le Nom Que Tu Veux Donner à ton Script": "nom_du_script,
}

Titre principal
st.sidebar.title("Scripts Linkuma")

Sous-titre et choix des scripts
st.sidebar.subheader("Les scripts")
selection = st.sidebar.radio("", list(PAGES.keys()), index=0)

Affichage du script sélectionné
page = PAGES[selection]
page.app()
