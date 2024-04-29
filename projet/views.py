from django.shortcuts import render, redirect
from map.models import SpatialProjet
from django.shortcuts import get_object_or_404
from .models import Projet, Commentaire, PartiPrenante, Photo
from django.http import JsonResponse
from itertools import chain
from .forms import CommentaireForm, PhotoForm


def load_data(request):
    # Récupérer tous les objets de Projet
    spatial = SpatialProjet.objects.all()

    # Créer une liste pour stocker les données
    geojson = []

    for elt in spatial:
        # Ajouter chaque objet et ses relations à la liste
        geojson.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(elt.longitude), float(elt.latitude)]
            },
            "properties": {
                "id": f"{elt.leprojet.id}",
                "date": f"{elt.leprojet.date_created}",
                "titre": f"{elt.leprojet.titre}",
                "descrip": f"{elt.leprojet.descrip_reduit}",
                "entreprise": f"{elt.leprojet.entreprise}",
                "delais": f"{elt.leprojet.delais_execution}",
                "financement": f"{elt.leprojet.financement}"
            }
        })

    # Retourner les données en tant que réponse JSON
    return JsonResponse(geojson, safe=False)


def home(request):
    projets = SpatialProjet.objects.all()
    projets = sorted(
        chain(projets),
        key=lambda instance: instance.leprojet.date_created,
        reverse=True
    )
    context = {
        "projets": projets
    }
    return render(request, 'map/map.html', context=context)


def projet_detail(request, projet_id):
    projet = get_object_or_404(Projet, id=projet_id)
    commentaire_1 = Commentaire.objects.filter(leprojet=projet)
    commentaire_1 = sorted(
        chain(commentaire_1),
        key=lambda instance: instance.date_created,
        reverse=True
    )
    autCont = PartiPrenante.objects.filter(projet=projet, role=PartiPrenante.AUTORITE_CONTRACTANTE)
    maitDvre = PartiPrenante.objects.filter(projet=projet, role=PartiPrenante.MAITRE_D_OUVRAGE)
    chefDmarch = PartiPrenante.objects.filter(projet=projet, role=PartiPrenante.CHEF_DU_MARCHE)
    ingDmarch = PartiPrenante.objects.filter(projet=projet, role=PartiPrenante.INGENIEUR_DU_MARCHE)
    maitDoevr = PartiPrenante.objects.filter(projet=projet, role=PartiPrenante.MAITRISE_D_OEUVRE)

    if request.method == 'POST':
        photo_form = PhotoForm(request.POST, request.FILES)
        commentaire_form = CommentaireForm(request.POST)
        if photo_form.is_valid() and commentaire_form.is_valid():
            photo = photo_form.save(commit=False)
            photo.uploader = request.user  # Remplacez par votre logique
            photo.save()

            commentaire = commentaire_form.save(commit=False)
            commentaire.leprojet = Projet.objects.get(id=projet_id)  # Remplacez par votre logique
            commentaire.commentateur = request.user  # Remplacez par votre logique
            commentaire.photo = photo
            commentaire.save()
            return redirect('view_projet', projet_id)
    else:
        photo_form = PhotoForm()
        commentaire_form = CommentaireForm()

    context = {
        "projet": projet,
        "commentaire": commentaire_1,
        "autCont": autCont,
        "maitDvre": maitDvre,
        "chefDmarch": chefDmarch,
        "ingDmarch": ingDmarch,
        "maitDoevr": maitDoevr,
        'photo_form': photo_form,
        'commentaire_form': commentaire_form
    }
    return render(request, "projet/projet_detail.html", context=context)


