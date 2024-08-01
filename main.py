import streamlit as st
import pandas as pd
import re
import io

st.set_page_config(page_title="Analyseur de texte", page_icon="📝")

spacy_available = False
try:
    import spacy
    spacy_available = True
except ImportError as e:
    st.error(f"Erreur lors de l'importation de spaCy: {e}")

# Fonction pour charger les modèles de langage
@st.cache_resource
def load_spacy_models():
    if not spacy_available:
        return None, None
    try:
        nlp_fr = spacy.load('fr_core_news_sm')
        nlp_en = spacy.load('en_core_web_sm')
        return nlp_fr, nlp_en
    except Exception as e:
        st.error(f"Erreur lors du chargement des modèles de langage: {e}")
        return None, None

# Chargement des modèles
nlp_fr, nlp_en = load_spacy_models() if spacy_available else (None, None)

# Fonction d'analyse de texte
def analyze_text(text, lang='fr'):
    if not spacy_available or (nlp_fr is None and nlp_en is None):
        return "Analyse de texte non disponible en raison de problèmes avec spaCy."
    
    nlp = nlp_fr if lang == 'fr' else nlp_en
    doc = nlp(text)
    # Votre logique d'analyse ici
    return f"Analyse effectuée pour le texte : {text[:50]}..."  # exemple de retour

# Interface utilisateur Streamlit
st.title("Analyseur de texte")

text_input = st.text_area("Entrez votre texte ici:")
lang_choice = st.radio("Choisissez la langue:", ('Français', 'Anglais'))

if st.button("Analyser"):
    if text_input:
        lang = 'fr' if lang_choice == 'Français' else 'en'
        result = analyze_text(text_input, lang)
        st.write(result)
    else:
        st.warning("Veuillez entrer du texte à analyser.")

# Affichage des informations de débogage
st.sidebar.title("Informations de débogage")
st.sidebar.write(f"spaCy disponible : {spacy_available}")
st.sidebar.write(f"Modèle français chargé : {nlp_fr is not None}")
st.sidebar.write(f"Modèle anglais chargé : {nlp_en is not None}")
