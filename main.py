import streamlit as st
import pandas as pd
import re

# Charger les thématiques depuis le fichier Excel
def load_thematiques(file_path):
    df_template = pd.read_excel(file_path)
    thematique_dict = {}
    current_thematique = None
    for index, row in df_template.iterrows():
        if pd.notna(row['THEMATIQUE FR']):
            current_thematique = row['THEMATIQUE FR']
            thematique_dict[current_thematique] = []
        if pd.notna(row['MENU FR']) and current_thematique:
            thematique_dict[current_thematique].append(row['MENU FR'])
    return thematique_dict

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

    # Charger les thématiques
    thematique_file_path = 'TEMPLATE THEMATIQUES.xlsx'
    thematiques = load_thematiques(thematique_file_path)
    
    # Ajustements et exclusion de certaines thématiques
    sensitive_keywords = ['religion', 'sex', 'voyance', 'escort']
    sensitive_regex = re.compile(r'\b(?:%s)\b' % '|'.join(map(re.escape, sensitive_keywords)), re.IGNORECASE)
    year_regex = re.compile(r'\b(19[0-9]{2}|20[0-9]{2})\b')

    # Saisie des noms de domaine
    domaines_input = st.text_area("Entrez les noms de domaine (un par ligne)")

    if st.button("Analyser"):
        if domaines_input:
            domaines = [domain.strip() for domain in domaines_input.split('\n') if domain.strip()]

            # Classifier les domaines
            classified_domains = []
            excluded_domains = []
            for domain in domaines:
                if sensitive_regex.search(domain) or year_regex.search(domain):
                    excluded_domains.append(domain)
                else:
                    category = classify_domain(domain, thematiques)
                    classified_domains.append((domain, category))
            
            # Créer le DataFrame pour les résultats
            df = pd.DataFrame(classified_domains, columns=['Domain', 'Category'])
            df_excluded = pd.DataFrame(excluded_domains, columns=['Domain'])
            df_excluded['Category'] = 'EXCLU'
            
            # Afficher la prévisualisation des résultats
            st.subheader("Prévisualisation des résultats")
            st.write(df)
            st.write(df_excluded)
            
            # Ajouter une option pour télécharger les résultats
            def convert_df_to_excel(df1, df2):
                output = pd.ExcelWriter('domaines_classes_resultats.xlsx', engine='xlsxwriter')
                df1.to_excel(output, index=False, sheet_name='Classified')
                df2.to_excel(output, index=False, sheet_name='Excluded')
                output.save()
                return output

            st.download_button(
                label="Télécharger les résultats en Excel",
                data=convert_df_to_excel(df, df_excluded).getvalue(),
                file_name="domaines_classes_resultats.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Veuillez entrer au moins un nom de domaine.")

if __name__ == "__main__":
    main()
