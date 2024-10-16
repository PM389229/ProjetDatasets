import openai
import os
from dotenv import load_dotenv

# Charger la clé API OpenAI depuis le fichier .env
env_path = r"C:\Users\User\Downloads\CoursAlternance\data\ProjetDatasets\src\DataSetsApp\hf.env"
print(f"Chargement du fichier .env depuis : {env_path}")
load_dotenv(dotenv_path=env_path)

openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    print("Erreur : La clé API OpenAI n'est pas définie.")
    exit(1)

# Créer un simple prompt pour tester la génération de texte
prompt = "Donne-moi un fait intéressant sur les pandas."


# Appel à l'API OpenAI en utilisant GPT-4
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Utilise GPT-4
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )

    # Afficher la réponse
    print(response['choices'][0]['message']['content'].strip())

except Exception as e:
    print(f"Erreur lors de l'appel à l'API OpenAI : {e}")
