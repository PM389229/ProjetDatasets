from hugchat import hugchat
from hugchat.login import Login
from dotenv import dotenv_values
import time
import logging

# Configurer les logs pour tout afficher
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def send_prompt_and_get_response(prompt):
    try:
        logging.info("Chargement des variables d'environnement depuis hf.env")
        # Charger les variables d'environnement
        secrets = dotenv_values('C:/Users/User/Downloads/CoursAlternance/data/ProjetDatasets/src/DataSetsApp/hf.env')

        hf_email = secrets.get('EMAIL')
        hf_pass = secrets.get('PASS')

        # Vérifier si les identifiants ont été trouvés
        if not hf_email or not hf_pass:
            logging.error("EMAIL ou PASS manquant dans le fichier .env")
            return

        logging.info(f"EMAIL trouvé: {hf_email}")
        logging.info("Début de l'authentification avec Hugging Face")

        # Connexion à Hugging Face
        sign = Login(hf_email, hf_pass)

        # Essai de login
        logging.info("Tentative de connexion via Login")
        cookies = sign.login()

        # Vérifier si les cookies ont été obtenus
        if cookies is None:
            logging.error("Cookies non obtenus : l'authentification a échoué.")
            return
        
        logging.debug(f"Cookies obtenus : {cookies}")

        # Ajouter un délai pour stabiliser la connexion
        logging.info("Ajout d'un délai pour stabiliser la connexion")
        time.sleep(2)

        # Créer une instance du ChatBot Hugging Face
        logging.info("Création de l'instance du chatbot")
        chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

        # Envoyer le prompt et obtenir la réponse
        logging.info(f"Envoi du prompt : {prompt}")
        response = chatbot.chat(prompt)
        
        # Vérifier la réponse du chatbot
        if response:
            logging.info(f"Réponse obtenue du chatbot : {response}")
        else:
            logging.error("Aucune réponse obtenue du chatbot.")

        # Afficher la réponse
        print("Réponse du bot :", response)

        return response

    except Exception as e:
        logging.error(f"Une erreur s'est produite : {e}", exc_info=True)

# Exemple d'utilisation
if __name__ == '__main__':
    prompt = "Donne-moi une phrase inspirante sur l'apprentissage."
    send_prompt_and_get_response(prompt)
