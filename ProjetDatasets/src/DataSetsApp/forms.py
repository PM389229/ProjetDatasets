from django import forms
from .models import Dataset
from django.contrib.auth.models import User, Group
from django.core.validators import FileExtensionValidator

# formulaire pour les datasets.
class DatasetForm(forms.ModelForm):
    # Champ de fichier avec validation pour accepter uniquement les fichiers CSV, JSON, et XML.
    fichier = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['csv', 'json'])]
    )
    description = forms.CharField(widget=forms.Textarea, required=False)
    
    
    # Informations de métadonnées pour le formulaire.
    class Meta:
        model = Dataset  # Modèle associé au formulaire
        fields = ['titre', 'fichier','fichier_type','Auteur','description']  # champs inclus dans le formulaire


    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        # Filtrer les utilisateurs du groupe "Professeurs"
        self.fields['Auteur'].queryset = User.objects.filter(groups__name='Professeurs')



# formulaire pour l'upload de dossiers d'images.
class ImageUploadForm(forms.Form):
    # Champ de texte pour le lien vers le dossier voulu.
    image_dir = forms.CharField(label='Lien vers le dossier voulu', max_length=255)
