import os
import csv
from pymongo import MongoClient

# Le script ici présent permet de transferer plusieurs csv d'un coup d'un dossier directement dans des collections créées à cet effet dans 
# une base de données 'my_database'



# Définition du chemin d'accès au répertoire contenant les fichiers CSV
csv_dir = "C:\\Users\\User\\Downloads\\CoursAlternance\\data\\ProjetDatasets\\src\\StockCSV"

# connection à MongoDB Express
client = MongoClient('mongodb://PM929:root@localhost:27017')

# On parcourt tous les fichiers CSV dans le répertoire
for csv_file in os.listdir(csv_dir):
    if csv_file.endswith('.csv'):
        # On va défibnir le chemin d'accès complet au fichier CSV
        csv_path = os.path.join(csv_dir, csv_file)

        # Puis créer une nouvelle collection pour le fichier CSV
        collection = client['my_database'][csv_file.replace('.csv', '')]

        # Et enfin on ouvre le fichier CSV et insère les données dans la collection
        with open(csv_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                collection.insert_one(row)

# Fermeture de la connexion à MongoDB Express
client.close()
