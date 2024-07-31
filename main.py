import streamlit as st
import pandas as pd
import re
import io
import string

# Dictionnaire des thématiques et mots-clés
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux', 'terriers'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier', 'fortune', 'credit'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones', 'research', 'graphics', 'solution'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux', 'solar', 'energy'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors', 'baby'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo', 'cricket'],
    'TOURISME': ['travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping', 'croisiere', 'location', 'tourisme', 'vacance', 'voyage', 'sauna', 'expat'],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture', 'formula']
}

# Mots clés pour exclure des domaines
excluded_keywords = ['religion', 'sex', 'voyance', 'escort', 'jesus', 'porn']
excluded_regex = re.compile(r'\b(?:%s)\b' % '|'.join(map(re.escape, excluded_keywords)), re.IGNORECASE)
year_regex = re.compile(r'\b(19[0-9]{2}|20[0-9]{2})\b')
name_regex = re.compile(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b')

def determine_language(domain):
    tld = domain.split('.')[-1]
    tld_to_lang = {
        'fr': 'FR', 'com': 'EN', 'uk': 'EN', 'de': 'DE', 'es': 'ES',
        'it': 'IT', 'ru': 'RU', 'cn': 'CN', 'net': 'EN', 'org': 'EN'
    }
    return tld_to_lang.get(tld, 'EN')

def classify_domain(domain, categories):
    domain_lower = domain.lower()
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in domain_lower:
                return category
    return 'NON UTILISÉ'

def is_excluded(domain):
    if excluded_regex.search(domain) or year_regex.search(domain):
        return True
    if name_regex.search(domain):
        return True
    if any(word in domain.lower() for word in ['pas cher', 'bas prix']):
        return True
    return False

def has_meaning(domain):
    # Supprime les extensions courantes et les caractères non-alphabétiques
    clean_domain = re.sub(r'\.(com|net|org|info|biz|fr|de|uk|es|it)$', '', domain.lower())
    clean_domain = ''.join(char for char in clean_domain if char.isalnum())
    
    # Vérifie si le domaine contient au moins un mot anglais de 3 lettres ou plus
    words = re.findall(r'\b\w{3,}\b', clean_domain)
    return len(words) > 0

def main():
    st.title("Classification des noms de domaine par thématique")
    
    domaines_input = st.text_area("Entrez les noms de domaine (un par ligne)")
    
    if st.button("Analyser"):
        if domaines_input:
            domaines = [domain.strip() for domain in domaines_input.split('\n') if domain.strip()]
            
            classified_domains = []
            excluded_and_non_utilise_domains = []
            
            for domain in domaines:
                if is_excluded(domain):
                    excluded_and_non_utilise_domains.append((domain, 'EXCLU', determine_language(domain)))
                else:
                    category = classify_domain(domain, thematique_dict)
                    language = determine_language(domain)
                    if category == 'NON UTILISÉ' and not has_meaning(domain):
                        excluded_and_non_utilise_domains.append((domain, 'EXCLU (pas de sens)', language))
                    elif category == 'NON UTILISÉ':
                        excluded_and_non_utilise_domains.append((domain, category, language))
                    else:
                        classified_domains.append((domain, category, language))
            
            df_classified = pd.DataFrame(classified_domains, columns=['Domain', 'Category', 'Language'])
            df_excluded_and_non_utilise = pd.DataFrame(excluded_and_non_utilise_domains, columns=['Domain', 'Category', 'Language'])
            
            st.subheader("Prévisualisation des résultats")
            st.write(df_classified)
            st.write(df_excluded_and_non_utilise)
            
            def convert_df_to_excel(df1, df2):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df1.to_excel(writer, index=False, sheet_name='Classified')
                    df2.to_excel(writer, index=False, sheet_name='Excluded and Non Utilisé')
                output.seek(0)
                return output

            st.download_button(
                label="Télécharger les résultats en Excel",
                data=convert_df_to_excel(df_classified, df_excluded_and_non_utilise),
                file_name="domaines_classes_resultats.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Veuillez entrer au moins un nom de domaine.")

if __name__ == "__main__":
    main()
