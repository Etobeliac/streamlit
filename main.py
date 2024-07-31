import streamlit as st
import pandas as pd
import re
import io

# Dictionnaire des thématiques et mots-clés
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones', 'file'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo'],
    'TOURISME': ['travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping', 'croisiere', 'location', 'tourisme', 'vacance', 'voyage', 'chamber'],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture']
}

# Mots clés pour exclure des domaines
excluded_keywords = ['religion', 'sex', 'voyance', 'escort', 'jesus']
excluded_regex = re.compile(r'\b(?:%s)\b' % '|'.join(map(re.escape, excluded_keywords)), re.IGNORECASE)
year_regex = re.compile(r'\b(19[0-9]{2}|20[0-9]{2})\b')

# Mots-clés pour déterminer les langues
language_keywords = {
    'EN': ['the', 'and', 'for', 'with', 'without', 'file', 'recipe', 'travel', 'health', 'beauty', 'fashion', 'sport', 'vehicle'],
    'FR': ['le', 'la', 'les', 'et', 'pour', 'sans', 'fichier', 'recette', 'voyage', 'santé', 'beauté', 'mode', 'sport', 'véhicule'],
    'DE': ['der', 'die', 'das', 'und', 'für', 'mit', 'ohne', 'datei', 'rezept', 'reise', 'gesundheit', 'schönheit', 'mode', 'sport', 'fahrzeug'],
    'ES': ['el', 'la', 'los', 'y', 'para', 'sin', 'archivo', 'receta', 'viaje', 'salud', 'belleza', 'moda', 'deporte', 'vehículo'],
    'IT': ['il', 'la', 'i', 'e', 'per', 'senza', 'file', 'ricetta', 'viaggio', 'salute', 'bellezza', 'moda', 'sport', 'veicolo'],
    'RU': ['и', 'для', 'без', 'файл', 'рецепт', 'путешествие', 'здоровье', 'красота', 'мода', 'спорт', 'автомобиль'],
    'CN': ['和', '文件', '配方', '旅行', '健康', '美容', '时尚', '运动', '车辆']
}

# Fonction pour déterminer la langue basée sur le TLD et les mots-clés
def determine_language(domain):
    tld = domain.split('.')[-1]
    if tld == 'fr':
        return 'FR'
    elif tld == 'de':
        return 'DE'
    elif tld == 'es':
        return 'ES'
    elif tld == 'it':
        return 'IT'
    elif tld == 'ru':
        return 'RU'
    elif tld == 'cn':
        return 'CN'
    else:
        # Vérifier les mots-clés dans le nom de domaine
        for lang, keywords in language_keywords.items():
            for keyword in keywords:
                if keyword in domain.lower():
                    return lang
        return ''  # Retourne une chaîne vide si aucune langue n'est déterminée

# Déterminer si un domaine contient un nom propre basé sur un ensemble de règles simples
def is_name(domain):
    parts = domain.split('.')
    name_patterns = re.compile(r'^[a-zA-Z]+(-[a-zA-Z]+)*$', re.IGNORECASE)
    if name_patterns.match(parts[0]):
        return True
    return False

# Classifier un domaine par thématique
def classify_domain(domain, categories):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in domain.lower():
                return category
    return 'NON UTILISÉ'

# Fonction principale pour le script Streamlit
def main():
    st.title("Classification des noms de domaine par thématique")
    
    # Saisie des noms de domaine
    domaines_input = st.text_area("Entrez les noms de domaine (un par ligne)")
    
    if st.button("Analyser"):
        if domaines_input:
            domaines = [domain.strip() for domain in domaines_input.split('\n') if domain.strip()]
            
            # Classifier les domaines
            classified_domains = []
            excluded_and_non_utilise_domains = []
            
            for domain in domaines:
                category = classify_domain(domain, thematique_dict)
                language = determine_language(domain)
                
                # Appliquer les règles extraites des commentaires
                if any(kw in domain for kw in excluded_keywords) or year_regex.search(domain) or is_name(domain):
                    excluded_and_non_utilise_domains.append((domain, 'EXCLU', language))
                else:
                    classified_domains.append((domain, category, language))
            
            # Créer le DataFrame pour les résultats
            df_classified = pd.DataFrame(classified_domains, columns=['Domain', 'Category', 'Language'])
            df_excluded_and_non_utilise = pd.DataFrame(excluded_and_non_utilise_domains, columns=['Domain', 'Category', 'Language'])
            
            # Afficher la prévisualisation des résultats
            st.subheader("Prévisualisation des résultats")
            st.write(df_classified)
            st.write(df_excluded_and_non_utilise)
            
            # Ajouter une option pour télécharger les résultats
            def convert_df_to_excel(df1, df2):
                output = io.BytesIO()
                writer = pd.ExcelWriter(output, engine='xlsxwriter')
                df1.to_excel(writer, index=False, sheet_name='Classified')
                df2.to_excel(writer, index=False, sheet_name='Excluded and Non Utilisé')
                writer.close()
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
