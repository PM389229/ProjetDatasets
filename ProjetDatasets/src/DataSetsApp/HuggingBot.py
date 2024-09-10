import re
import json
from hugchat import hugchat
from hugchat.login import Login
from dotenv import load_dotenv
import os
import time

def extract_json_from_text(text):
    # Utiliser une expression régulière pour extraire le contenu entre les délimiteurs ````json``
    match = re.search(r'```json(.*?)```', text, re.DOTALL)
    if match:
        json_text = match.group(1).strip()
        return json_text
    return None


def generate_dataset_with_bot(prompt):
    # Charger les variables d'environnement
    env_path = r"C:\Users\User\Downloads\CoursAlternance\data\ProjetDatasets\src\DataSetsApp\hf.env"
    load_dotenv(dotenv_path=env_path)

    hf_email = os.getenv('EMAIL')
    hf_pass = os.getenv('PASS')

    # Connexion à Hugging Face
    sign = Login(hf_email, hf_pass)
    cookies = sign.login()

    # Convertir RequestsCookieJar en dictionnaire
    cookies_dict = cookies.get_dict()

    # Ajouter un délai pour la sécurité
    time.sleep(2)

    # Créer le ChatBot avec les cookies convertis en dictionnaire
    chatbot = hugchat.ChatBot(cookies=cookies_dict)

    # Générer le dataset avec le prompt
    response = chatbot.chat(prompt)

    # Convertir la réponse en chaîne de caractères directement (supposant que la réponse est du texte)
    response_text = str(response)

    # Extraire le JSON du texte
    json_text = extract_json_from_text(response_text)

    if json_text:
        # Charger le texte JSON dans une structure Python
        try:
            json_data = json.loads(json_text)
            return json_data
        except json.JSONDecodeError as e:
            print(f"Erreur lors du chargement du JSON: {e}")
            return None
    else:
        print("Aucun JSON trouvé dans la réponse.")
        return None
