# models.py

from django.db import models
from django.conf import settings


#Modele pr representer les meta données d'un Dataset
class Dataset(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mots_clefs = models.TextField(blank=True, null=True)
    fichier = models.FileField(upload_to='datasets/')
    fichier_type = models.CharField(max_length=10, choices=(('csv', 'CSV'), ('json', 'JSON')))
    file_size = models.BigIntegerField(null=True, blank=True)
    Auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    HeureChargement = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dataset(metadata)'
        app_label = 'DataSetsApp'
        managed = True

# Modele pour une image
class Image(models.Model):
    image_name = models.CharField(max_length=255)
    image_data = models.BinaryField()
    file_size = models.BigIntegerField(null=True, blank=True)
    Auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    HeureChargement = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image'
        app_label = 'DataSetsApp'
        managed = True




class ImageFolderMetadata(models.Model):
    folder_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mots_clefs = models.TextField(blank=True, null=True)
    fichier_type = models.CharField(max_length=10)
    file_size = models.BigIntegerField(null=True, blank=True)
    Auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    HeureChargement = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'datasetimagefolder(metadata)'
        app_label = 'DataSetsApp'
        managed = True