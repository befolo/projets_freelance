from django.shortcuts import render
from .models import Projet
from map.models import SpatialProjet
from django.http import JsonResponse


def load_data(request):
    # Récupérer tous les objets de Projet
    spatial = SpatialProjet.objects.all()

    # Créer une liste pour stocker les données
    features = []

    for elt in spatial:
        # Ajouter chaque objet et ses relations à la liste
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(elt.longitude), float(elt.latitude)]
            },
            "properties": {
                "titre": f"{elt.leprojet.titre}",
                "descrip": f"{elt.leprojet.descrip_reduit}",
                "entreprise": f"{elt.leprojet.entreprise}",
                "delais": f"{elt.leprojet.delais_execution}",
                "financement": f"{elt.leprojet.financement}"
            }
        })

    # Créer le GeoJSON final
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    # Retourner les données en tant que réponse JSON
    return JsonResponse(geojson, safe=False)


def home(request):
    context = {
        "data": 14
    }
    return render(request, 'map/map.html', context=context)
