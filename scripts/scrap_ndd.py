import streamlit as st
import pandas as pd
import io

def app():
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
            # Classification des domaines (ici, c'est juste un exemple)
            df['Catégorie'] = 'Exemple'
            
            st.success("Classification terminée !")

            # Affichage des résultats
            st.write("Résultats de la classification :")
            st.dataframe(df)

            # Préparation du fichier Excel pour le téléchargement
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Domaines classifiés', index=False)
            output.seek(0)

            # Bouton de téléchargement
            st.download_button(
                label="Télécharger les résultats (Excel)",
                data=output,
                file_name="domaines_classes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    app()
