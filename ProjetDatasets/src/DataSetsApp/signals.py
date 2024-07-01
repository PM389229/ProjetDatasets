from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.db.models.signals import post_migrate
from django.dispatch import receiver

# Import de User et Group ,
#  User est le modèle standard pour les utilisateurs et Group lui , est utilisé pour gérer des groupes d'users


# post_save, post_migrate :  signaux Django  envoyés par le système de modèles de Django à certains points :
# post_save après la sauvegarde d'un modèle et post_migrate après l'exécution des migrations.

# receiver : Un décorateur utilisé pour indiquer qu'une fonction donnée doit recevoir des signaux.

# Création de deux gestionnaires de signaux Django pour automatiser des actions pendant la migration de la BDD 
# et de la création de nouveaux utilisateurs


@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    Group.objects.get_or_create(name='Professeurs')


@receiver(post_save, sender=User)
def handle_user_created(sender, instance, created, **kwargs):
    if created:
      
        pass