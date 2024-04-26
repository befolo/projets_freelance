from django.shortcuts import render


# creer un fonctions qui convertira le contenus de la table Projet dans un fichier csv


def view_map(request):
    return render(request, 'map/map.html')
