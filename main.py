import streamlit as st
import pandas as pd
import re
import io
from gensim.models import KeyedVectors
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Charger le modèle pré-entraîné de Word2Vec de Google News
word2vec_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)

# Dictionnaire des thématiques et mots-clés (combinaison des anciens et nouveaux)
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux', 'terriers', 'veterinary', 'breed', 'wildlife', 'dog', 'cat', 'bird', 'fish', 'monde marin'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant', 'chef', 'gastronomy', 'dining', 'eatery', 'kitchen', 'bakery', 'catering', 'madeleine', 'plat'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services', 'firm', 'industry', 'commerce', 'trade', 'venture', 'market', 'publicity'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier', 'fortune', 'credit', 'money', 'invest', 'mortgage', 'loan', 'tax', 'insurance', 'wealth'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones', 'research', 'graphics', 'solution', 'hardware', 'programming', 'coding', 'digital', 'cyber', 'web', 'hack', 'forum', 'apps', 'digital', 'open media', 'email', 'AI', 'machine learning', 'competence'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux', 'solar', 'energy', 'decor', 'furniture', 'property', 'apartment', 'condo', 'villa', '4piecesetplus'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping', 'style', 'clothing', 'accessories', 'women', 'hat', 'jewelry', 'makeup', 'designer', 'boutique', 'shopping', 'runway', 'model'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors', 'baby', 'therapy', 'massage', 'biochemie', 'skincare'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo', 'cricket', 'gym', 'athletic', 'team', 'league', 'club', 'cycling', 'surf', 'trail', 'marathon', 'tango'],
    'TOURISME': ['travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping', 'croisiere', 'location', 'tourisme', 'vacance', 'voyage', 'sauna', 'expat', 'visit', 'explore', 'adventure', 'destination', 'hotel', 'resort', 'photo', 'document', 'wave', 'land', 'fries', 'voyage', 'trip', 'journey', 'escape', 'getaway'],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture', 'formula', 'drive', 'racing', 'garage', 'repair', 'dealership', 'rental', 'taxi', 'bus', 'train', 'plane', 'aviation']
}

# Mots clés pour exclure des domaines (combinaison des anciens et nouveaux)
excluded_keywords = ['religion', 'sex', 'voyance', 'escort', 'jesus', 'porn', 'teen', 'adult', 'White Pussy', 'Black Cocks', 'youtube', 'instagram', 'pinterest', 'forex', 'trading', 'invest', 'broker', 'stock', 'market', 'finance', 'avocat']
excluded_regex = re.compile(r'\b(?:%s)\b' % '|'.join(map(re.escape, excluded_keywords)), re.IGNORECASE)
year_regex = re.compile(r'\b(19[0-9]{2}|20[0-9]{2})\b')
name_regex = re.compile(r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b')
brand_regex = re.compile(r'\b(samsung|atari|longchamp)\b', re.IGNORECASE)
geographic_regex = re.compile(r'\b(louisville|quercy|france|ferney)\b', re.IGNORECASE)
publicity_regex = re.compile(r'\bpublicity\b', re.IGNORECASE)
transport_regex = re.compile(r'\btransport\b', re.IGNORECASE)

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
                # Prioritize certain keywords over others
                if category == 'SANTE' and 'skincare' in domain_lower:
                    return 'SANTE'
                # Exclude domains that contain 'land' if 'ecole' is present
                if category == 'TOURISME' and 'land' in domain_lower and 'ecole' in domain_lower:
                    return 'EXCLU'
                return category

    # Use semantic similarity with Word2Vec and cosine similarity
    domain_vector = np.mean([word2vec_model[word] for word in domain_lower.split() if word in word2vec_model], axis=0)
    if domain_vector is None:
        return 'NON UTILISE'

    category_vectors = {}
    for category, keywords in categories.items():
        category_vector = np.mean([word2vec_model[word] for word in keywords if word in word2vec_model], axis=0)
        if category_vector is not None:
            category_vectors[category] = category_vector

    for category, category_vector in category_vectors.items():
        similarity = cosine_similarity([domain_vector], [category_vector])
        if similarity > 0.5:  # Adjust the threshold as needed
            return category

    return 'NON UTILISE'

def is_excluded(domain):
    if excluded_regex.search(domain) or year_regex.search(domain):
        return True
    if name_regex.search(domain):
        return True
    if any(word in domain.lower() for word in ['pas cher', 'bas prix']):
        return True
    if re.search(r'\b[a-z]+[A-Z][a-z]+\b', domain):  # Probable proper names
        return True
    if len(domain.split('.')[0]) <= 3:  # Very short domains
        return True
    if brand_regex.search(domain):  # Brands
        return True
    if geographic_regex.search(domain):  # Geographic
        return True
    if publicity_regex.search(domain) and not transport_regex.search(domain):
        return True
    return False

def has_meaning(domain):
    clean_domain = re.sub(r'\.(com|net|org|info|biz|fr|de|uk|es|it)$', '', domain.lower())
    clean_domain = ''.join(char for char in clean_domain if char.isalnum())
    words = re.findall(r'\b\w{3,}\b', clean_domain)
    return len(words) > 0

def main():
    st.title("Classification des noms de domaine par thématique")

    domaines_input = st.text_area("Entrez les noms de domaine (un par ligne)")

    if st.button("Analyser"):
        if domaines_input:
            domaines = [domain.strip() for domain in domaines_input.split('\n') if domain.strip()]
            classified_domains = []
            excluded_domains = []

            for domain in domaines:
                language = determine_language(domain)

                try:
                    if is_excluded(domain):
                        excluded_domains.append((domain, 'EXCLU', language))
                    else:
                        category = classify_domain(domain, thematique_dict)
                        if category == 'NON UTILISE' and not has_meaning(domain):
                            excluded_domains.append((domain, 'EXCLU (pas de sens)', language))
                        elif category == 'NON UTILISE':
                            excluded_domains.append((domain, category, language))
                        else:
                            classified_domains.append((domain, category, language))
                except Exception as e:
                    st.error(f"Erreur lors de l'analyse du domaine {domain}: {e}")

            df_classified = pd.DataFrame(classified_domains, columns=['Domain', 'Category', 'Language'])
            df_excluded = pd.DataFrame(excluded_domains, columns=['Domain', 'Category', 'Language'])

            st.subheader("Prévisualisation des résultats")
            st.write(df_classified)
            st.write(df_excluded)

            def convert_df_to_excel(df1, df2):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df1.to_excel(writer, index=False, sheet_name='Classified')
                    df2.to_excel(writer, index=False, sheet_name='Excluded')
                output.seek(0)
                return output

            st.download_button(
                label="Télécharger les résultats en Excel",
                data=convert_df_to_excel(df_classified, df_excluded),
                file_name="domaines_classes_resultats.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Veuillez entrer au moins un nom de domaine.")

if __name__ == "__main__":
    main()
