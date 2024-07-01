class DatabaseRouter:
    """
    Un routeur pour contrôler toutes les opérations de base de données sur les modèles dans
    l'application DataSetsApp pour utiliser MongoDB.
    """

    # Définir les étiquettes des applications pour lesquelles ce routeur est applicable
    route_app_labels = {'DataSetsApp'}

    def db_for_read(self, model, **hints):
        """
        Dirige les opérations de lecture vers la base de données appropriée.
        
        :param model: Le modèle pour lequel une opération de lecture est effectuée
        :param hints: Des indices supplémentaires fournis lors de l'opération
        :return: Le nom de la base de données à utiliser pour les opérations de lecture
        """
        # Vérifie si le modèle appartient à l'application spécifiée
        if model._meta.app_label in self.route_app_labels:
            # Si le modèle est 'image', utiliser 'my_database_images'
            if model._meta.model_name == 'image':
                return 'my_database_images'
            else:
                # Sinon, utiliser 'my_database'
                return 'my_database'
        # Par défaut, utiliser la base de données 'default'
        return 'default'

    def db_for_write(self, model, **hints):
        """
        Dirige les opérations d'écriture vers la base de données appropriée.
        
        :param model: Le modèle pour lequel une opération d'écriture est effectuée
        :param hints: Des indices supplémentaires fournis lors de l'opération
        :return: Le nom de la base de données à utiliser pour les opérations d'écriture
        """
        # Vérifie si le modèle appartient à l'application spécifiée
        if model._meta.app_label in self.route_app_labels:
            # Si le modèle est 'image', utiliser 'my_database_images'
            if model._meta.model_name == 'image':
                return 'my_database_images'
            else:
                # Sinon, utiliser 'my_database'
                return 'my_database'
        # Par défaut, utiliser la base de données 'default'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Détermine si une relation entre deux objets est autorisée.
        
        :param obj1: Le premier objet
        :param obj2: Le deuxième objet
        :param hints: Des indices supplémentaires fournis lors de l'opération
        :return: True si la relation est autorisée, sinon None
        """
        # Permettre les relations si l'un des objets appartient à l'application spécifiée
        if obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
            return True
        # Sinon, renvoie None pour utiliser le comportement par défaut
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Détermine si une opération de migration est autorisée dans une base de données spécifique.
        
        :param db: Le nom de la base de données
        :param app_label: L'étiquette de l'application
        :param model_name: Le nom du modèle (optionnel)
        :param hints: Des indices supplémentaires fournis lors de l'opération
        :return: True si la migration est autorisée, sinon False
        """
        # Vérifie si l'application est spécifiée pour ce routeur
        if app_label in self.route_app_labels:
            # Si le modèle est 'image', permettre la migration uniquement dans 'my_database_images'
            if model_name == 'image':
                return db == 'my_database_images'
            else:
                # Sinon, permettre la migration dans 'my_database'
                return db == 'my_database'
        # Par défaut, permettre la migration dans la base de données 'default'
        return db == 'default'
