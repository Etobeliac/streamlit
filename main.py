import streamlit as st
import pandas as pd
import re
import io
import spacy

# Charger les modèles de langage
@st.cache_resource
def load_spacy_models():
    try:
        nlp_fr = spacy.load('fr_core_news_sm')
        nlp_en = spacy.load('en_core_web_sm')
        return nlp_fr, nlp_en
    except Exception as e:
        st.error(f"Erreur lors du chargement des modèles de langage: {e}")
        return None, None

nlp_fr, nlp_en = load_spacy_models()

if nlp_fr is None or nlp_en is None:
    st.error("Impossible de charger les modèles de langage. L'application ne peut pas fonctionner correctement.")
    st.stop()

# Le reste de votre code ici...

# Exemple de fonction utilisant spaCy
def analyze_text(text, lang='fr'):
    nlp = nlp_fr if lang == 'fr' else nlp_en
    doc = nlp(text)
    # Votre logique d'analyse ici
    return doc

# Interface utilisateur Streamlit
st.title("Analyseur de texte")

text_input = st.text_area("Entrez votre texte ici:")
lang_choice = st.radio("Choisissez la langue:", ('Français', 'Anglais'))

if st.button("Analyser"):
    if text_input:
        lang = 'fr' if lang_choice == 'Français' else 'en'
        result = analyze_text(text_input, lang)
        st.write("Analyse terminée !")
        # Affichez les résultats de l'analyse ici
    else:
        st.warning("Veuillez entrer du texte à analyser.")
