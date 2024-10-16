import requests
import os
import re
import csv
from dotenv import load_dotenv

def generate_dataset_with_bot(prompt, num_rows=5, num_columns=2, output_format='json'):
    # Charger les variables d'environnement pour le token Hugging Face
    env_path = r"C:\Users\User\Downloads\CoursAlternance\data\ProjetDatasets\src\DataSetsApp\hf.env"
    load_dotenv(dotenv_path=env_path)
    hf_token = os.getenv('HF_API_TOKEN')

    if not hf_token:
        print("Erreur : Le token d'API Hugging Face n'est pas défini.")
        return None

    # Utiliser un modèle plus adapté à la génération structurée
    model_id = "text-davinci-003"  # Exemple de modèle plus puissant
    headers = {
        "Authorization": f"Bearer {hf_token}"
    }

    # Prompt détaillé, y compris le prompt personnalisé et les lignes/colonnes
    structured_prompt = (
        f"{prompt}\n\n"  # Prompt personnalisé
        f"Génère un dataset JSON de {num_rows} lignes et {num_columns} colonnes. "
        "Les champs doivent inclure des informations sur la consommation de vin des pays, avec les colonnes 'Pays', 'Année', 'Consommation (litres)', etc."
    )

    data = {
        "inputs": structured_prompt
    }

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

        # Utiliser une regex pour extraire la partie JSON
        json_match = re.search(r'\[.*?\]', dataset_text, re.DOTALL)

        if json_match:
            json_text = json_match.group(0)
            print(f"JSON extrait : {json_text}")

            try:
                dataset_json = eval(json_text)  # Ou json.loads(json_text)
                return dataset_json
            except Exception as e:
                print(f"Erreur lors de la conversion en JSON : {e}")
                return None
        else:
            print("Aucun JSON valide trouvé.")
            return None
    else:
        print(f"Erreur lors de la requête API : {response.status_code} - {response.text}")
        return None



def json_to_csv(json_data, output_file='dataset_huggingface.csv'):
    if isinstance(json_data, list) and len(json_data) > 0:
        # Supposons que les colonnes soient toujours "Nom" et "Âge"
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nom', 'Âge'])
            for row in json_data:
                writer.writerow([row.get('Nom', ''), row.get('Âge', '')])
        print(f"Dataset exporté en CSV : {output_file}")
    else:
        print("Données JSON invalides ou vides.")
