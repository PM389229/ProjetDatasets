import os
from pymongo import MongoClient
from bson import binary


#Le script suivant permet de transferer un dossier d'images de différents types directement dans une collection mongoDB que l'on propose
# de télécharger après dans 'datasets'





# on va définir ici le chemin d'accès au répertoire contenant les fichiers images que l'on veut mettre dans la collection
image_dir = "C:\\Users\\User\\Downloads\\CoursAlternance\\data\\ProjetDatasets\\src\\StockCSV\\StockImages\\faces3"

# connection à MongoDB Express
client = MongoClient('mongodb://PM929:root@localhost:27017')

# boucle pour parcourir tous les fichiers image dans le répertoire
for image_file in os.listdir(image_dir):
    if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
        # Définition du chemin d'accès complet au fichier ciblé
        image_path = os.path.join(image_dir, image_file)

        # On crée une nouvelle collection pour le fichier que l'on veut (ou on utilise la collection existante)
        collection = client['my_database_images']['images3(410)']

        # ouverture du fichier voulu + insertion des données binaires dans la collection
        with open(image_path, 'rb') as file:
            encoded_image = binary.Binary(file.read())
            image_document = {
                'image_name': image_file,
                'image_data': encoded_image
            }
            collection.insert_one(image_document)

# fermeture de  la connexion à MongoDB Express
client.close()
