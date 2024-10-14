from django import forms
from .models import Dataset
from django.contrib.auth.models import User, Group
from django.core.validators import FileExtensionValidator

# Formulaire pour les datasets
class DatasetForm(forms.ModelForm):
    # Champ de fichier avec validation pour accepter uniquement les fichiers CSV et JSON.
    fichier = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'json'])]
    )
    description = forms.CharField(widget=forms.Textarea, required=False)
    mots_clefs = forms.CharField(
        widget=forms.Textarea, 
        required=False, 
        label='Mots Clefs', 
        help_text='Ajoutez des mots-clés pour décrire le dataset.'
    )
    
    # Informations de métadonnées pour le formulaire
    class Meta:
        model = Dataset  # Modèle associé au formulaire
        fields = ['titre', 'fichier', 'description', 'mots_clefs']  # Champs inclus dans le formulaire


# Formulaire pour l'upload de dossiers d'images
class ImageUploadForm(forms.Form):
    image_dir = forms.CharField(label='Lien vers le dossier voulu', max_length=255)
    fichier_type = forms.ChoiceField(
        label='Type de fichier',
        choices=[('png', 'PNG'), ('jpg', 'JPG'),('webp', 'WEBP'), ('gif', 'GIF'), ('tiff', 'TIFF')]
    )
    description = forms.CharField(widget=forms.Textarea, required=False, label='Description')
    mots_clefs = forms.CharField(
        widget=forms.Textarea, 
        required=False, 
        label='Mots Clefs', 
        help_text='Ajoutez des mots-clés pour décrire le dossier d\'images.'
    )


# Formulaire pour création de datasets avec Hugging Face avec données réelles
class DatasetCreationForm(forms.ModelForm):
    fichier_type = forms.ChoiceField(choices=[('csv', 'CSV'), ('json', 'JSON')])
    prompt = forms.CharField(widget=forms.Textarea, label='Prompt', help_text='Entrez le prompt pour générer le dataset.')
    mots_clefs = forms.CharField(
        widget=forms.Textarea, 
        required=False, 
        label='Mots Clefs', 
        help_text='Ajoutez des mots-clés pour décrire le dataset généré.'
    )
    
    class Meta:
        model = Dataset
        fields = ['titre', 'description', 'fichier_type', 'prompt', 'mots_clefs']