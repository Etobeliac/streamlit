import streamlit as st
import pandas as pd

# Définir les thématiques et leurs mots-clés
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo'],
    'TOURISME': ['travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping', 'croisiere', 'location', 'tourisme', 'vacance', 'voyage'],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture']
}

# Fonction pour classifier un domaine
def classify_domain(domain, categories):
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in domain.lower():
                return category
    return 'NON UTILISÉ'

# Fonction pour vérifier les domaines à exclure
def is_excluded(domain):
    exclusions = ['religious', 'sex', 'voyance', 'escort']
    if any(exclusion in domain.lower() for exclusion in exclusions):
        return True
    if any(char.isdigit() for char in domain):
        return True
    return False

# Interface Streamlit
st.title("Classification de Noms de Domaine")

domains_input = st.text_area("Entrez les noms de domaine séparés par des virgules")
domains_list = [domain.strip() for domain in domains_input.split(",") if domain.strip()]

if st.button("Classifier"):
    classified_domains = []
    excluded_domains = []
    
    for domain in domains_list:
        if is_excluded(domain):
            excluded_domains.append(domain)
        else:
            category = classify_domain(domain, thematique_dict)
            classified_domains.append((domain, category))

    df_classified = pd.DataFrame(classified_domains, columns=['Domain', 'Category'])
    df_excluded = pd.DataFrame(excluded_domains, columns=['Domain'])
    
    st.subheader("Prévisualisation avant classification")
    st.write(df_classified)
    
    st.subheader("Domaines exclus")
    st.write(df_excluded)
    
    if st.button("Télécharger le résultat"):
        output_file = 'domaines_classes_resultats.xlsx'
        with pd.ExcelWriter(output_file) as writer:
            df_classified.to_excel(writer, sheet_name='Classified', index=False)
            df_excluded.to_excel(writer, sheet_name='Excluded', index=False)
        
        st.success(f"Le fichier a été sauvegardé sous le nom : {output_file}")
        st.download_button(
            label="Télécharger le fichier Excel",
            data=open(output_file, 'rb').read(),
            file_name=output_file,
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
