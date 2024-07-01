import os
import csv
from pymongo import MongoClient
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Dataset
from .forms import DatasetForm, ImageUploadForm
from django.http import HttpResponse
from django.conf import settings
import io
import tempfile
import zipfile
from zipfile import ZipFile
import json
import xml.etree.ElementTree as ET
import re
from bson import json_util
from bson import binary

#Constante pour dossiers d'images

MONGO_URI = 'mongodb://PM929:root@localhost:27017'


# Configuration des identifiants pour la connection à MongoDB
MONGO_USERNAME = 'PM929'
MONGO_PASSWORD = 'root'

# Vue pour la page d'accueil
def home(request):

    return render(request, 'DataSetsApp/home.html')




# fonction pour ajouter un utilisateur au groupe "Professeurs"
def add_user_to_professors_group(username):

    user = User.objects.get(username=username)

    group = Group.objects.get(name='Professeurs')
    # Ajout de l'utilisateur au groupe
    group.user_set.add(user)



# Vue pour la gestion de l'inscription des utilisateurs
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
            user = form.save()
            
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # Redirection vers la page d'accueil après l'inscription
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})






@login_required
@csrf_exempt
def upload_image_folder(request):
    if not request.user.groups.filter(name='Professeurs').exists():
        return HttpResponse('Accès non autorisé', status=403)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST)
        if form.is_valid():
            image_dir = form.cleaned_data['image_dir']
            try:
                # Vérifiez que le répertoire existe sur le serveur
                if not os.path.exists(image_dir):
                    return HttpResponse(f"Directory {image_dir} does not exist", status=400)
                
                # Uploader les images depuis le répertoire
                upload_images_to_mongo(image_dir, MONGO_URI)
                return HttpResponse('Upload successful!')
            except Exception as e:
                return HttpResponse(f"Error during upload: {e}", status=500)
    else:
        form = ImageUploadForm()
    return render(request, 'datasets/upload_image_folder.html', {'form': form})




def upload_images_to_mongo(image_dir, mongo_uri):
    client = MongoClient(mongo_uri)
    collection_name = os.path.basename(image_dir)
    db_name = 'my_database_images'
    collection = client[db_name][collection_name]

    for image_file in os.listdir(image_dir):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(image_dir, image_file)
            with open(image_path, 'rb') as file:
                encoded_image = binary.Binary(file.read())
                image_document = {
                    'image_name': image_file,
                    'image_data': encoded_image
                }
                collection.insert_one(image_document)

    client.close()




@login_required
def upload_dataset(request):
    if not request.user.groups.filter(name='Professeurs').exists():
        return HttpResponse('Accès non autorisé', status=403)
    
    if request.method == 'POST':
        form = DatasetForm(request.POST, request.FILES)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.uploaded_by = request.user
            dataset.save()

            fichier = request.FILES['fichier']
            fichier_type = fichier.name.split('.')[-1]

            client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
            db = client['my_database']  # Base de données pour les datasets
            collection_name = dataset.titre.replace(" ", "_").lower()
            collection = db[collection_name]

            # Nettoyez la collection avant d'insérer de nouveaux documents
            collection.delete_many({})

            # Utilisez les fonctions appropriées pour insérer les données des fichiers
            if fichier_type == 'csv':
                handle_csv(fichier, collection)
            elif fichier_type == 'json':
                handle_json(fichier, collection)

            client.close()
            return redirect('list_datasets')
    else:
        form = DatasetForm()
    return render(request, 'datasets/upload_dataset.html', {'form': form})




def handle_csv(fichier, collection):
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'utf-16']
    for encoding in encodings:
        try:
            fichier.seek(0)
            csv_data = fichier.read().decode(encoding)
            csv_reader = csv.DictReader(io.StringIO(csv_data))
            for row in csv_reader:
                collection.insert_one(row)
            break
        except (UnicodeDecodeError, StopIteration):
            continue

def handle_json(fichier, collection):
    try:
        fichier.seek(0)
        file_data = fichier.read().decode('utf-8')
        json_data = json.loads(file_data)
        if isinstance(json_data, list):
            collection.insert_many(json_data)
        else:
            collection.insert_one(json_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON file: {str(e)}")
    except Exception as e:
        raise ValueError(f"An unexpected error occurred: {str(e)}")



@login_required
def list_datasets(request):
    query = request.GET.get('q', '').lower()
    client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')

    # Accéder à la base de données
    db = client['my_database']

    # Récupérer les métadonnées
    metadata_collection = db['dataset(metadata)']
    metadata_list = list(metadata_collection.find())
    metadata_dict = {metadata['titre'].replace(" ", "_").lower(): metadata for metadata in metadata_list}

    # Filtrer les métadonnées par description si une requête est fournie
    if query:
        filtered_metadata_list = [metadata for metadata in metadata_list if query in metadata.get('description', '').lower()]
    else:
        filtered_metadata_list = metadata_list

    # Construire la liste des datasets avec leurs métadonnées et échantillons
    datasets = []
    for metadata in filtered_metadata_list:
        collection_name = metadata['titre'].replace(" ", "_").lower()
        dataset_sample = list(db[collection_name].find().limit(3))  # Récupérer les trois premières lignes
        metadata['formatted_titre'] = metadata['titre'].replace(" ", "_").lower()
        
        # Récupérer l'utilisateur par ID
        try:
            user = User.objects.get(id=metadata['Auteur_id'])
            metadata['Auteur'] = user.username
        except User.DoesNotExist:
            metadata['Auteur'] = "Utilisateur inconnu"
        
        datasets.append({
            'metadata': metadata,
            'sample': dataset_sample
        })

    # Recherche dans la base de données des dossiers d'images
    db_images = client['my_database_images']
    all_collections_images = db_images.list_collection_names()
    if query:
        collection_names_images = [name for name in all_collections_images if query in name.lower()]
    else:
        collection_names_images = all_collections_images

    client.close()

    return render(request, 'datasets/list_datasets.html', {
        'datasets': datasets,
        'collection_names_images': collection_names_images,
        'query': query
    })






# Vue pour télécharger toutes les images d'une collection spécifique
@login_required
def download_all_images(request, image_collection_name):
    client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
    db = client['my_database_images']
    collection = db[image_collection_name]
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'w') as zip_file:
        for image in collection.find():
            img_name = image['image_name']
            img_data = image['image_data']
            zip_file.writestr(img_name, img_data)
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{image_collection_name}.zip"'
    client.close()
    return response





def download_data(request, collection_name, fichier_type):
    client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
    db = client['my_database']
    collection = db[collection_name]
    documents = list(collection.find())

    if fichier_type == 'json':
        # Utiliser json_util pour sérialiser les documents MongoDB
        response = HttpResponse(json.dumps(documents, default=json_util.default), content_type='application/json')
        response['Content-Disposition'] = f'attachment; filename="{collection_name}.json"'
    elif fichier_type == 'xml':
        root = ET.Element('Data')
        for document in documents:
            item = ET.SubElement(root, 'Item')
            for key, value in document.items():
                child = ET.SubElement(item, key)
                child.text = str(value)
        xmlstr = ET.tostring(root, encoding='utf-8', method='xml')
        response = HttpResponse(xmlstr, content_type='application/xml')
        response['Content-Disposition'] = f'attachment; filename="{collection_name}.xml"'
    else:  # Assume CSV as a default or fallback
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{collection_name}.csv"'
        writer = csv.writer(response)
        if documents:
            headers = documents[0].keys()
            writer.writerow(headers)
            for document in documents:
                writer.writerow([document.get(h, '') for h in headers])

    client.close()
    return response