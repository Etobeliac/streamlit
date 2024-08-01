import streamlit as st
import pandas as pd
import re
import io

st.set_page_config(page_title="Analyseur de texte", page_icon="📝")

try:
    import spacy
    spacy_available = True
except ImportError as e:
    st.error(f"Erreur lors de l'importation de spaCy: {e}")
    spacy_available = False

# Fonction pour charger les modèles spaCy
def load_spacy_models():
    if spacy_available:
        try:
            nlp_fr = spacy.load("fr_core_news_sm")
            nlp_en = spacy.load("en_core_web_sm")
            return nlp_fr, nlp_en
        except Exception as e:
            st.error(f"Erreur lors du chargement des modèles spaCy: {e}")
            return None, None
    return None, None

nlp_fr, nlp_en = load_spacy_models()

# Fonction pour analyser le texte
def analyze_text(text, nlp):
    if not spacy_available or nlp is None:
        return "Analyse non disponible : spaCy n'est pas chargé correctement."
    
    doc = nlp(text)
    
    # Analyse des entités nommées
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    
    # Analyse syntaxique
    syntax = [(token.text, token.pos_, token.dep_) for token in doc]
    
    # Tokens et lemmas
    tokens_lemmas = [(token.text, token.lemma_) for token in doc]
    
    return {
        "entities": entities,
        "syntax": syntax,
        "tokens_lemmas": tokens_lemmas
    }

# Interface utilisateur Streamlit
st.title("Analyseur de texte")

text_input = st.text_area("Entrez votre texte ici :")
language = st.selectbox("Choisissez la langue :", ["Français", "English"])

if st.button("Analyser"):
    if text_input:
        nlp = nlp_fr if language == "Français" else nlp_en
        results = analyze_text(text_input, nlp)
        
        if isinstance(results, str):
            st.write(results)
        else:
            st.subheader("Entités nommées")
            st.write(results["entities"])
            
            st.subheader("Analyse syntaxique")
            st.write(results["syntax"])
            
            st.subheader("Tokens et lemmas")
            st.write(results["tokens_lemmas"])
    else:
        st.warning("Veuillez entrer du texte à analyser.")

# Fonction pour télécharger les résultats
def download_results(results):
    output = io.StringIO()
    output.write("Entités nommées:\n")
    for ent in results["entities"]:
        output.write(f"{ent[0]}: {ent[1]}\n")
    
    output.write("\nAnalyse syntaxique:\n")
    for token in results["syntax"]:
        output.write(f"{token[0]}: {token[1]} ({token[2]})\n")
    
    output.write("\nTokens et lemmas:\n")
    for token in results["tokens_lemmas"]:
        output.write(f"{token[0]}: {token[1]}\n")
    
    return output.getvalue()

if 'results' in locals() and isinstance(results, dict):
    if st.button("Télécharger les résultats"):
        results_text = download_results(results)
        st.download_button(
            label="Télécharger les résultats en format texte",
            data=results_text,
            file_name="resultats_analyse.txt",
            mime="text/plain"
        )
