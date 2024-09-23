import os
import csv
from pymongo import MongoClient
from django.shortcuts import render, redirect , get_object_or_404 
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import Dataset , ImageFolderMetadata
from .forms import DatasetForm, ImageUploadForm , DatasetCreationForm
from .HuggingBot import generate_dataset_with_bot
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
from bson.objectid import ObjectId
import logging
from PIL import Image
import io

logger = logging.getLogger(__name__)
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
            fichier_type = form.cleaned_data['fichier_type']
            description = form.cleaned_data['description']
            mots_clefs = form.cleaned_data['mots_clefs']
            try:
                if not os.path.exists(image_dir):
                    return HttpResponse(f"Directory {image_dir} does not exist", status=400)

                # Calculer la taille totale des fichiers image dans le répertoire en KB
                total_size = sum(os.path.getsize(os.path.join(image_dir, f)) for f in os.listdir(image_dir) if f.lower().endswith(f'.{fichier_type}'))
                total_size_kb = total_size / (1024*1024) # Conversion en megaoctets

                # Uploader les images depuis le répertoire
                upload_images_to_mongo(image_dir, MONGO_URI, request.user, fichier_type)

                # Enregistrer les métadonnées du dossier, y compris la taille en MB
                folder_name = os.path.basename(image_dir)
                ImageFolderMetadata.objects.create(
                    folder_name=folder_name,
                    description=description,
                    mots_clefs=mots_clefs,
                    fichier_type=fichier_type,
                    Auteur=request.user,
                    file_size=total_size_kb  # Taille en kilooctets
                )
                return redirect('list_datasets')
            except Exception as e:
                return HttpResponse(f"Error during upload: {e}", status=500)
    else:
        form = ImageUploadForm()
    return render(request, 'datasets/upload_image_folder.html', {'form': form})









def upload_images_to_mongo(image_dir, mongo_uri, user, fichier_type):
    client = MongoClient(mongo_uri)
    collection_name = os.path.basename(image_dir)
    db_name = 'my_database_images'
    collection = client[db_name][collection_name]

    for image_file in os.listdir(image_dir):
        if image_file.lower().endswith(f'.{fichier_type}'):
            image_path = os.path.join(image_dir, image_file)
            with open(image_path, 'rb') as file:
                encoded_image = binary.Binary(file.read())

                # Générer une miniature avec PIL
                with Image.open(image_path) as img:
                    img.thumbnail((100, 100))

                    thumb_io = io.BytesIO()

                    # Utiliser 'JPEG' au lieu de 'JPG' pour PIL
                    if fichier_type.upper() == 'JPG':
                        img_format = 'JPEG'
                    else:
                        img_format = fichier_type.upper()

                    img.save(thumb_io, format=img_format)
                    encoded_thumb = binary.Binary(thumb_io.getvalue())

                # Insérer à la fois l'image originale et la miniature
                image_document = {
                    'image_name': image_file,
                    'image_data': encoded_image,
                    'thumbnail_data': encoded_thumb  # Stocker la miniature
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
            dataset.Auteur = request.user

            fichier = request.FILES['fichier']
            fichier_type = fichier.name.split('.')[-1].lower()

            # Calculer la taille du fichier en kilooctets
            file_size = fichier.size / (1024 * 1024)  # Conversion en kilooctets

            if fichier_type in ['csv', 'json']:
                dataset.fichier_type = fichier_type
            else:
                return HttpResponse("Type de fichier non supporté", status=400)

            dataset.file_size = file_size  # Enregistrer la taille du fichier en KB
            dataset.save()

            client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
            db = client['my_database']
            collection_name = dataset.titre.replace(" ", "_").lower()
            collection = db[collection_name]

            # Nettoyez la collection avant d'insérer de nouveaux documents
            collection.delete_many({})

            # Utiliser les fonctions appropriées pour insérer les données
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


def is_professor(user):
    return user.groups.filter(name='Professeurs').exists()






@login_required
@user_passes_test(is_professor)
def delete_image_folder(request, folder_name):
    logger.info(f"Received folder_name: {folder_name}")

    try:
        # Connexion à MongoDB avec authentification
        client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
        db_metadata = client['my_database']
        db_images = client['my_database_images']

        # Vérifier si le dossier d'images existe dans les métadonnées
        folder_metadata = db_metadata['datasetimagefolder(metadata)'].find_one({'folder_name': folder_name})
        if not folder_metadata:
            logger.error(f"Folder metadata not found for folder_name: {folder_name}")
            return HttpResponse(f"Dossier d'images non trouvé: {folder_name}", status=404)

        logger.info(f"Found folder metadata: {folder_metadata}")

        # Suppression de la collection d'images
        logger.info(f"Deleting image collection: {folder_name}")
        db_images.drop_collection(folder_name)

        # Suppression des métadonnées dans MongoDB
        logger.info(f"Deleting metadata in MongoDB for folder: {folder_name}")
        db_metadata['datasetimagefolder(metadata)'].delete_one({'folder_name': folder_name})

        client.close()

        return redirect('list_datasets')
    except Exception as e:
        logger.error(f"Erreur lors de la suppression du dossier d'images: {e}")
        return HttpResponse(f"Erreur lors de la suppression: {e}", status=500)








@login_required
def list_datasets(request):
    query = request.GET.get('q', '').lower()
    file_type = request.GET.get('file_type', '').lower()
    client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')

    try:
        # Connexion à la base de données MongoDB pour les métadonnées et les images
        db_metadata = client['my_database']
        db_images = client['my_database_images']  # Définition de db_images ici
        metadata_collection = db_metadata['dataset(metadata)']
        image_folder_metadata_collection = db_metadata['datasetimagefolder(metadata)']

        # Obtenir toutes les métadonnées des datasets texte et images
        metadata_list = list(metadata_collection.find())
        image_folder_metadata_list = list(image_folder_metadata_collection.find())

        all_results = []

        # Traiter les datasets texte
        for metadata in metadata_list:
            collection_name = metadata['titre'].replace(" ", "_").lower()
            dataset_sample = list(db_metadata[collection_name].find().limit(3))
            metadata['formatted_titre'] = collection_name

            try:
                user = User.objects.get(id=metadata['Auteur_id'])
                metadata['Auteur'] = user.username
            except User.DoesNotExist:
                metadata['Auteur'] = "Utilisateur inconnu"

            metadata['id'] = str(metadata['_id'])
            all_results.append({'type': 'text', 'metadata': metadata, 'sample': dataset_sample})

        # Traiter les dossiers d'images
        for metadata in image_folder_metadata_list:
            try:
                user = User.objects.get(id=metadata['Auteur_id'])
                metadata['Auteur'] = user.username
            except User.DoesNotExist:
                metadata['Auteur'] = "Utilisateur inconnu"

            metadata['id'] = str(metadata['_id'])

            # Récupérer un échantillon d'images (miniatures) depuis la collection d'images
            image_collection = db_images[metadata['folder_name']]  # db_images est maintenant défini
            sample_images = list(image_collection.find({}, {'image_data': 1, 'image_name': 1}).limit(3))

            all_results.append({'type': 'image', 'metadata': metadata, 'sample': sample_images})

        # Appliquer les filtres de recherche
        if query or file_type:
            filtered_results = []
            for item in all_results:
                metadata = item['metadata']
                matches_query = query in metadata.get('description', '').lower() or query in metadata.get('titre', '').lower() or query in metadata.get('folder_name', '').lower() or query in metadata.get('mots_clefs', '').lower()
                matches_file_type = file_type == metadata.get('fichier_type', '').lower() if file_type else True
                if matches_query and matches_file_type:
                    filtered_results.append(item)
        else:
            filtered_results = all_results

        is_professor = request.user.groups.filter(name='Professeurs').exists()

        return render(request, 'datasets/list_datasets.html', {
            'all_results': filtered_results,
            'query': query,
            'file_type': file_type,
            'is_professor': is_professor
        })
    finally:
        client.close()









def is_professor(user):
    return user.groups.filter(name='Professeurs').exists()






@login_required
@user_passes_test(is_professor)
def delete_dataset(request, dataset_id):
    try:
        client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
        db = client['my_database']
        metadata_collection = db['dataset(metadata)']

        # Supprimer les métadonnées du dataset
        result = metadata_collection.find_one_and_delete({"_id": ObjectId(dataset_id)})
        if not result:
            client.close()
            return HttpResponse("Dataset non trouvé", status=404)

        # Supprimer la collection associée
        collection_name = result['titre'].replace(" ", "_").lower()
        db.drop_collection(collection_name)

        client.close()
        return redirect('list_datasets')
    except Exception as e:
        return HttpResponse(f"Erreur lors de la suppression: {e}", status=500)







@login_required
def generate_dataset_view(request):
    if request.method == 'POST':
        form = DatasetCreationForm(request.POST)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.Auteur = request.user

            prompt = form.cleaned_data['prompt']
            fichier_type = form.cleaned_data['fichier_type']

            # Générer les données avec le bot
            bot_response = generate_dataset_with_bot(prompt)

            if bot_response:  # Vérifier si le JSON a été chargé correctement
                # Connexion à MongoDB
                client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
                db = client['my_database']
                collection_name = dataset.titre.replace(" ", "_").lower()
                collection = db[collection_name]

                try:
                    if fichier_type == 'json':
                        # Insertion dans la base de données
                        collection.insert_many(bot_response if isinstance(bot_response, list) else [bot_response])
                    elif fichier_type == 'csv':
                        # Traiter la réponse CSV
                        reader = csv.DictReader(bot_response.splitlines())
                        for row in reader:
                            collection.insert_one(row)
                except Exception as e:
                    return render(request, 'datasets/generate_dataset.html', {'form': form, 'error': str(e)})

                # Sauvegarder le dataset et fermer la connexion MongoDB
                dataset.save()
                client.close()
                return redirect('view_dataset')
            else:
                return render(request, 'datasets/generate_dataset.html', {'form': form, 'error': "Erreur dans la réponse du bot."})
    else:
        form = DatasetCreationForm()

    return render(request, 'datasets/generate_dataset.html', {'form': form})





@login_required
def view_dataset_view(request):
    generated_data = request.session.get('generated_data')
    form_data = request.session.get('form_data')

    if not generated_data:
        return redirect('generate_dataset')  # Rediriger si aucune donnée n'est présente

    if request.method == 'POST':
        form = DatasetCreationForm(request.POST)
        if form.is_valid():
            dataset = form.save(commit=False)
            dataset.Auteur = request.user

            fichier_type = form.cleaned_data['fichier_type']

            # Connecter à MongoDB
            client = MongoClient(f'mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@localhost:27017/')
            db = client['my_database']
            collection_name = dataset.titre.replace(" ", "_").lower()
            collection = db[collection_name]

            try:
                if fichier_type == 'json':
                    json_data = json.loads(generated_data)
                    collection.insert_many(json_data if isinstance(json_data, list) else [json_data])
                elif fichier_type == 'csv':
                    reader = csv.DictReader(generated_data.splitlines())
                    collection.insert_many(list(reader))
            except Exception as e:
                return render(request, 'datasets/view_dataset.html', {'form': form, 'generated_data': generated_data, 'error': str(e)})

            dataset.save()
            client.close()
            return redirect('list_datasets')
    else:
        form = DatasetCreationForm(form_data)  # Remplir le formulaire avec les données précédentes

    return render(request, 'datasets/view_dataset.html', {'form': form, 'generated_data': generated_data})






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