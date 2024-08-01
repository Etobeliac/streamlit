import streamlit as st
import pandas as pd
import re
import io
import string

# Dictionnaire des thématiques et mots-clés (combinaison des anciens et nouveaux)
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux', 'terriers', 'veterinary', 'breed', 'wildlife', 'dog', 'cat', 'bird', 'fish'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant', 'chef', 'gastronomy', 'dining', 'eatery', 'kitchen', 'bakery', 'catering'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services', 'firm', 'industry', 'commerce', 'trade', 'venture', 'market', 'publicity'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier', 'fortune', 'credit', 'money', 'invest', 'mortgage', 'loan', 'tax', 'insurance', 'wealth'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones', 'research', 'graphics', 'solution', 'hardware', 'programming', 'coding', 'digital', 'cyber', 'web', 'hack', 'forum', 'apps', 'digital', 'open media', 'email', 'AI', 'machine learning'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux', 'solar', 'energy', 'decor', 'furniture', 'property', 'apartment', 'condo', 'villa'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping', 'style', 'clothing', 'accessories', 'women', 'hat', 'jewelry', 'makeup', 'designer', 'boutique', 'shopping', 'runway', 'model'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors', 'baby', 'therapy', 'massage', 'biochimie', 'skincare'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo', 'cricket', 'gym', 'athletic', 'team', 'league', 'club', 'cycling', 'surf', 'trail'],
    'TOURISME': ['travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping', 'croisiere', 'location', 'tourisme', 'vacance', 'voyage', 'sauna', 'expat', 'visit', 'explore', 'adventure', 'destination', 'hotel', 'resort', 'photo', 'documed', 'wave', 'land', 'fries', 'voyage', 'trip', 'journey', 'escape', 'getaway'],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture', 'formula', 'drive', 'racing', 'garage', 'repair', 'dealership', 'rental', 'taxi', 'bus', 'train', 'plane', 'aviation']
}

# Mots clés pour exclure des domaines (combinaison des anciens et nouveaux)
excluded_keywords = ['religion', 'sex', 'voyance', 'escort', 'jesus', 'porn', 'teen', 'adult', 'White Pussy', 'Black Cocks', 'youtube', 'instagram', 'pinterest']
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
    return 'NON UTILISÉ'

def is_excluded(domain):
    if excluded_regex.search(domain) or year_regex.search(domain):
        return True
    if name_regex.search(domain):
        return True
    if any(word in domain.lower() for word in ['pas cher', 'bas prix']):
        return True
    if re.search(r'\b[a-z]+[A-Z][a-z]+\b', domain):  # Noms propres probables
        return True
    if len(domain.split('.')[0]) <= 3:  # Domaines très courts
        return True
    if brand_regex.search(domain):  # Marques
        return True
    if geographic_regex.search(domain):  # Géographique
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
