import streamlit as st
import pandas as pd
import re
import io

# Dictionnaire des thématiques et mots-clés
thematique_dict = {
    'ANIMAUX': ['animal', 'pet', 'zoo', 'farm', 'deer', 'chiens', 'chats', 'animaux', 'terriers', 'veterinary', 'breed', 'wildlife', 'dog', 'cat', 'bird', 'fish', 'monde marin'],
    'CUISINE': ['cook', 'recipe', 'cuisine', 'food', 'bon plan', 'equipement', 'minceur', 'produit', 'restaurant', 'chef', 'gastronomy', 'dining', 'eatery', 'kitchen', 'bakery', 'catering', 'madeleine', 'plat'],
    'ENTREPRISE': ['business', 'enterprise', 'company', 'corporate', 'formation', 'juridique', 'management', 'marketing', 'services', 'firm', 'industry', 'commerce', 'trade', 'venture', 'market', 'publicity'],
    'FINANCE / IMMOBILIER': ['finance', 'realestate', 'investment', 'property', 'assurance', 'banque', 'credits', 'immobilier', 'fortune', 'credit', 'money', 'invest', 'mortgage', 'loan', 'tax', 'insurance', 'wealth'],
    'INFORMATIQUE': ['tech', 'computer', 'software', 'IT', 'high tech', 'internet', 'jeux-video', 'marketing', 'materiel', 'smartphones', 'research', 'graphics', 'solution', 'hardware', 'programming', 'coding', 'digital', 'cyber', 'web', 'hack', 'forum', 'apps', 'digital', 'open media', 'email', 'AI', 'machine learning', 'competence'],
    'MAISON': ['home', 'house', 'garden', 'interior', 'deco', 'demenagement', 'equipement', 'immo', 'jardin', 'maison', 'piscine', 'travaux', 'solar', 'energy', 'decor', 'furniture', 'property', 'apartment', 'condo', 'villa', '4piecesetplus'],
    'MODE / FEMME': ['fashion', 'beauty', 'cosmetics', 'woman', 'beaute', 'bien-etre', 'lifestyle', 'mode', 'shopping', 'style', 'clothing', 'accessories', 'women', 'hat', 'jewelry', 'makeup', 'designer', 'boutique', 'shopping', 'runway', 'model'],
    'SANTE': ['health', 'fitness', 'wellness', 'medical', 'hospital', 'grossesse', 'maladie', 'minceur', 'professionnels', 'sante', 'seniors', 'baby', 'therapy', 'massage', 'biochimie', 'skincare'],
    'SPORT': ['sport', 'fitness', 'football', 'soccer', 'basketball', 'tennis', 'autre sport', 'basket', 'combat', 'foot', 'musculation', 'velo', 'cricket', 'gym', 'athletic', 'team', 'league', 'club', 'cycling', 'surf', 'trail', 'marathon', 'tango'],
    'TOURISME': ['travel', 'tourism', 'holiday', 'vacation', 'bon plan', 'camping', 'croisiere', 'location', 'tourisme', 'vacance', 'voyage', 'sauna', 'expat', 'visit', 'explore', 'adventure', 'destination', 'hotel', 'resort', 'photo', 'documed', 'wave', 'land', 'fries', 'voyage', 'trip', 'journey', 'escape', 'getaway'],
    'VEHICULE': ['vehicle', 'car', 'auto', 'bike', 'bicycle', 'moto', 'produits', 'securite', 'voiture', 'formula', 'drive', 'racing', 'garage', 'repair', 'dealership', 'rental', 'taxi', 'bus', 'train', 'plane', 'aviation']
}

# Fonction simplifiée pour classifier les domaines
def classify_domain(domain):
    domain_lower = domain.lower()
    for category, keywords in thematique_dict.items():
        if any(keyword in domain_lower for keyword in keywords):
            return category
    return 'NON UTILISÉ'

def main():
    st.title("Classification des noms de domaine par thématique")

    domaines_input = st.text_area("Entrez les noms de domaine (un par ligne)")

    if st.button("Analyser"):
        if domaines_input:
            domaines = [domain.strip() for domain in domaines_input.split('\n') if domain.strip()]

            classified_domains = [(domain, classify_domain(domain)) for domain in domaines]

            df_classified = pd.DataFrame(classified_domains, columns=['Domain', 'Category'])

            st.subheader("Prévisualisation des résultats")
            st.write(df_classified)

            def convert_df_to_excel(df):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Classified')
                output.seek(0)
                return output

            st.download_button(
                label="Télécharger les résultats en Excel",
                data=convert_df_to_excel(df_classified),
                file_name="domaines_classes_resultats.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Veuillez entrer au moins un nom de domaine.")

if __name__ == "__main__":
    main()
