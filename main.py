import streamlit as st
import os

# Chemin du dossier contenant les scripts
SCRIPTS_FOLDER = 'scripts'

# Titre de l'application
st.title("Scripts Viewer")

# Lister les fichiers dans le dossier des scripts et filtrer uniquement les fichiers
scripts = [f for f in os.listdir(SCRIPTS_FOLDER) if os.path.isfile(os.path.join(SCRIPTS_FOLDER, f))]

# Afficher la liste des scripts à gauche
selected_script = st.sidebar.selectbox("Select a script", scripts)

# Lire et afficher le contenu du script sélectionné
if selected_script:
    script_path = os.path.join(SCRIPTS_FOLDER, selected_script)
    with open(script_path, 'r') as file:
        script_content = file.read()
    st.subheader(f"Content of {selected_script}")
    st.code(script_content, language='python')
else:
    st.subheader("Select a script to view its content")

# Ajouter un bouton pour exécuter le script classifier.py
if st.button("Run classifier.py"):
    os.system('streamlit run scripts/classifier.py')
