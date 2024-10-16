from huggingface_hub import InferenceClient
from dotenv import dotenv_values
import logging

# Configurer les logs
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_prompt_and_get_response(prompt):
    try:
        logging.info("Chargement des variables d'environnement depuis hf.env")
        # Charger les variables d'environnement
        secrets = dotenv_values('C:/Users/User/Downloads/CoursAlternance/data/ProjetDatasets/src/DataSetsApp/hf.env')

        hf_api_token = secrets.get('HF_API_TOKEN')
        if not hf_api_token:
            raise Exception("HF_API_TOKEN non trouvé dans le fichier .env")

        logging.info("HF_API_TOKEN trouvé")

        # Créer une instance du client d'inférence Hugging Face
        client = InferenceClient(model="facebook/bart-large", token=hf_api_token)
        logging.info("Client d'inférence créé avec succès")

        # Envoyer le prompt et obtenir la réponse
        logging.info(f"Envoi du prompt : {prompt}")
        response = client.text_generation(prompt, max_new_tokens=50)  # Limiter la génération à 50 tokens
        logging.debug(f"Réponse brute de l'API : {response}")

        # Afficher la réponse telle qu'elle est, car il s'agit de texte brut
        logging.info(f"Réponse du bot : {response}")
        
        # Afficher la réponse
        print("Réponse du bot :", response)

        return response

    except Exception as e:
        logging.error(f"Une erreur s'est produite : {e}", exc_info=True)

# Exemple d'utilisation
if __name__ == '__main__':
    prompt = "Donne-moi une phrase inspirante sur l'apprentissage."
    send_prompt_and_get_response(prompt)
