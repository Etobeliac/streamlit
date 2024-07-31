from flask import Flask, render_template_string, request
import os

app = Flask(__name__)

# Chemin du dossier contenant les scripts
SCRIPTS_FOLDER = 'scripts'

# Template HTML pour l'interface
html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scripts Viewer</title>
    <style>
        body {
            display: flex;
            font-family: Arial, sans-serif;
        }
        #sidebar {
            width: 200px;
            padding: 10px;
            border-right: 1px solid #ccc;
        }
        #content {
            flex-grow: 1;
            padding: 10px;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 5px 0;
        }
        a {
            text-decoration: none;
            color: #000;
        }
        a:hover {
            text-decoration: underline;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border: 1px solid #ccc;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <div id="sidebar">
        <h3>Scripts</h3>
        <ul>
            {% for script in scripts %}
                <li>
                    <a href="/?script={{ script }}">{{ script }}</a>
                </li>
            {% endfor %}
        </ul>
    </div>
    <div id="content">
        {% if selected_script %}
            <h3>Content of {{ selected_script }}</h3>
            <pre>{{ script_content }}</pre>
        {% else %}
            <h3>Select a script to view its content</h3>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    # Lister les fichiers dans le dossier des scripts
    scripts = os.listdir(SCRIPTS_FOLDER)
    selected_script = request.args.get('script', None)
    script_content = ''
    
    # Lire le contenu du script sélectionné
    if selected_script:
        with open(os.path.join(SCRIPTS_FOLDER, selected_script), 'r') as file:
            script_content = file.read()
    
    return render_template_string(html_template, scripts=scripts, script_content=script_content, selected_script=selected_script)

if __name__ == '__main__':
    app.run(debug=True)
