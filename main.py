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

# Reste du code...
