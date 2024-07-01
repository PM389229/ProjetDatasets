# models.py

from django.db import models
from django.conf import settings


#Modele pr representer un Dataset
class Dataset(models.Model):
    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='datasets/')
    fichier_type = models.CharField(max_length=10, choices=(('csv', 'CSV'), ('json', 'JSON'), ('xml', 'XML')))
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dataset(metadata)'
        app_label = 'DataSetsApp'
        managed = True

# Modele pour une image
class Image(models.Model):
    image_name = models.CharField(max_length=255)
    image_data = models.BinaryField()
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image'
        app_label = 'DataSetsApp'
        managed = True
