import streamlit as st
import pandas as pd
import io
import os

def classify_domain(domain):
    # Ici, vous pouvez implémenter votre logique de classification réelle
    # Pour l'instant, nous utilisons une classification aléatoire
    import random
    categories = ['ANIMAUX', 'CUISINE', 'ENTREPRISE', 'FINANCE / IMMOBILIER', 'INFORMATIQUE', 
                  'MAISON', 'MODE / FEMME', 'SANTE', 'SPORT', 'TOURISME', 'VEHICULE', 'NON UTILISÉ']
    return random.choice(categories)

def main():
    st.set_page_config(layout="wide", page_title="Classification de Domaines")

    project_dir = os.path.dirname(os.path.abspath(__file__))
    script_dir = os.path.join(project_dir, 'script')
    script_files = [f for f in os.listdir(script_dir) if f.endswith('.py')]

    st.title("Classification de Domaines")

    # Zone de texte pour coller les noms de domaine
    domain_input = st.text_area("Collez vos noms de domaine ici (un par ligne)", height=200)

    if domain_input:
        # Conversion du texte en DataFrame
        domains = [domain.strip() for domain in domain_input.split('\n') if domain.strip()]
        df = pd.DataFrame({'Domaine': domains})

        st.write("Aperçu des données :")
        st.dataframe(df.head())

        if st.button("Classifier les domaines"):
            # Classification des domaines
            df['Catégorie'] = df['Domaine'].apply(classify_domain)
            
            st.success("Classification terminée !")

            # Comptage des résultats
            used_domains = df[df['Catégorie'] != 'NON UTILISÉ']
            not_used_domains = df[df['Catégorie'] == 'NON UTILISÉ']

            st.write(f"Domaines classifiés : {len(used_domains)}")
            st.write(f"Domaines non utilisés : {len(not_used_domains)}")

            # Affichage des résultats
            st.write("Résultats de la classification :")
            st.dataframe(df)

            # Préparation du fichier Excel pour le téléchargement
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                used_domains.to_excel(writer, sheet_name='Domaines classifiés', index=False)
                not_used_domains.to_excel(writer, sheet_name='Domaines non utilisés', index=False)
            output.seek(0)

            # Bouton de téléchargement
            st.download_button(
                label="Télécharger les résultats (Excel)",
                data=output,
                file_name="domaines_classes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    # Sélection du script dans la barre latérale (sans afficher le contenu)
    st.sidebar.title("Scripts disponibles")
    st.sidebar.selectbox("Sélectionnez un script :", script_files)

if __name__ == "__main__":
    main()
