import streamlit as st

def app():
    st.title("Classification de Domaines")
    st.write("Bienvenue dans l'application de classification des domaines.")

    # Lecture du fichier de thématiques
    file_path = 'TEMPLATE THEMATIQUES.xlsx'
    if not os.path.exists(file_path):
        st.error(f"Le fichier {file_path} n'existe pas. Veuillez le placer dans le même répertoire que le script.")
        return

    df_template = pd.read_excel(file_path)

    # Extraire les thématiques et les menus
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

    def classify_domain(domain, categories):
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in domain.lower():
                    return category
        return 'NON UTILISÉ'

    # Mise à jour des mots-clés en fonction des ajustements
    adjustments_file = 'domaines_classes_mises_a_jour.xlsx'
    if os.path.exists(adjustments_file):
        adjustments = pd.read_excel(adjustments_file)[['Domain', 'Ce que j'aurais mis ']].dropna()
        for index, row in adjustments.iterrows():
            domain = row['Domain']
            new_category = row['Ce que j'aurais mis ']
            if new_category in thematique_dict:
                thematique_dict[new_category].append(domain.split('.')[0].replace('-', '').lower())

    # Zone de texte pour coller les noms de domaine
    domain_input = st.text_area("Collez vos noms de domaine ici (un par ligne)", height=200)

    if domain_input:
        # Conversion du texte en liste de domaines
        domaines = [domain.strip() for domain in domain_input.split('\n') if domain.strip()]

        if st.button("Classifier les domaines"):
            # Classification des domaines
            classified_domains = [(domain, classify_domain(domain, thematique_dict)) for domain in domaines]

            # Création du DataFrame
            df = pd.DataFrame(classified_domains, columns=['Domain', 'Category'])

            # Séparation des domaines utilisés et non utilisés
            df_used = df[df['Category'] != 'NON UTILISÉ']
            df_not_used = df[df['Category'] == 'NON UTILISÉ']

            # Ajout des domaines non utilisés dans une nouvelle colonne
            df_final = df_used.copy()
            df_final['Non Utilisé'] = pd.NA
            df_final = pd.concat([df_final, pd.DataFrame({'Domain': pd.NA, 'Category': pd.NA, 'Non Utilisé': df_not_used['Domain']})], ignore_index=True)

            st.success("Classification terminée !")

            # Affichage des résultats
            st.write("Résultats de la classification :")
            st.dataframe(df_final)

            # Préparation du fichier Excel pour le téléchargement
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_final.to_excel(writer, index=False)
            output.seek(0)

            # Bouton de téléchargement
            st.download_button(
                label="Télécharger les résultats (Excel)",
                data=output,
                file_name="domaines_classes_mises_a_jour.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
