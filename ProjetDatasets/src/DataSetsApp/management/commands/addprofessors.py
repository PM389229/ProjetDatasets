from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group


# Script pour ajouter des Users au groupe 'Professeurs' qui permet de specifier l'accèes a 'upload_dataset'

class Command(BaseCommand):
    help = 'Assigns specified users to the Professors group'

    def handle(self, *args, **options):
        # Création du Groupe
        group, created = Group.objects.get_or_create(name='Professeurs')
        if created:
            self.stdout.write(self.style.SUCCESS('Successfully created group Professeurs'))
        
       
        professor_usernames = ['Stephane', 'Tatiana']  #On peut ajouter ici les Users que l'on veut comme Professeurs

        for username in professor_usernames:
            try:
                user = User.objects.get(username=username)
                group.user_set.add(user)
                self.stdout.write(self.style.SUCCESS(f'Successfully added {username} to Professeurs'))
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'User {username} does not exist'))

