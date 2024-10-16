import requests
import os
import csv
import re
import json
import time
from dotenv import load_dotenv

# Charger les variables d'environnement
env_path = r"C:\Users\User\Downloads\CoursAlternance\data\ProjetDatasets\src\DataSetsApp\hf.env"
print(f"Chargement du fichier .env depuis : {env_path}")
load_dotenv(dotenv_path=env_path)

# Récupérer le token depuis le fichier .env
hf_token = os.getenv('HF_API_TOKEN')

if not hf_token:
    print("Erreur : Le token d'API Hugging Face n'est pas défini.")
    exit(1)  # Terminer le script si le token n'est pas trouvé
else:
    print(f"Token chargé avec succès : {hf_token[:10]}***")  # Masquer partiellement le token pour la sécurité

# Définir le modèle et les headers d'API
model_id = "gpt-3.5-turbo"  # Exemple de modèle, à remplacer si nécessaire

headers = {
    "Authorization": f"Bearer {hf_token}"
}

# Créer un prompt structuré pour générer des données CSV
data = {
    "inputs": (
        "Crée un tableau de données CSV avec 50 lignes et 5 colonnes. "
        "Les colonnes doivent être : 'Nom', 'Âge', 'Ville', 'Profession' et 'Salaire'. "
        "Sépare chaque colonne par une virgule. Donne seulement les données, sans explication."
    )
}

# Fonction pour vérifier l'état du modèle et attendre si nécessaire
def check_model_ready(model_id, headers):
    while True:
        # Vérifier si le modèle est prêt
        response = requests.get(f"https://api-inference.huggingface.co/models/{model_id}", headers=headers)
        status = response.json()
        if 'estimated_time' in status:
            print(f"Modèle en cours de chargement. Temps estimé : {status['estimated_time']} secondes.")
            time.sleep(5)  # Attendre 5 secondes avant de réessayer
        else:
            print("Modèle prêt à être utilisé.")
            break

# Vérifier si le modèle est prêt
check_model_ready(model_id, headers)

# Faire une requête POST vers l'API Hugging Face
response = requests.post(
    f"https://api-inference.huggingface.co/models/{model_id}",
    headers=headers,
    json=data
)

# Vérifier la réponse de l'API
if response.status_code == 200:
    print("Réponse API reçue :")
    generated_data = response.json()

    # Extraire le texte généré
    dataset_text = generated_data[0]['generated_text']
    print(f"Dataset généré : {dataset_text}")

    # Utiliser une regex pour extraire uniquement les portions JSON bien formatées
    json_match = re.search(r'\[\{.*?\}\]', dataset_text)  # Cherche une occurrence JSON complète entre crochets

    if json_match:
        json_text = json_match.group(0)
        print(f"JSON extrait : {json_text}")

        # Tenter de charger chaque bloc comme JSON
        try:
            dataset_json = json.loads(json_text)  # Utiliser json.loads() pour convertir en JSON
            print(f"Dataset JSON : {dataset_json}")

            # Créer un fichier CSV et y écrire les données
            with open("dataset_huggingface.csv", mode="w", newline='', encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(["Nom", "Âge"])  # En-têtes de colonnes

                # Écrire les lignes du dataset dans le CSV
                for item in dataset_json:
                    writer.writerow([item.get("Nom", ""), item.get("Âge", "")])

            print("Le dataset a été exporté en CSV : dataset_huggingface.csv")
        except json.JSONDecodeError as e:
            print(f"Erreur lors de la conversion en JSON : {e}")
    else:
        print("Aucun JSON valide trouvé.")
else:
    print(f"Erreur lors de la requête API : {response.status_code} - {response.text}")
