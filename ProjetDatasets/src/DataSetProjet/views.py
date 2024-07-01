from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

#On definit ici une viex de test qui renvoie un simple Titre

# def vue_de_test(request):
#   return HttpResponse("<h1>Vue de Test</>")


#Ici la page d'accueil on utilise render pour recuperer la template en question
#avec context on récupère un dictionnaire qui nous permet de passer des clefs et des valeurs avec {} ,exemple avec datetime
# def index(request):
#   return render(request, "DataSetProjet/index.html", context={"date": datetime.today()})