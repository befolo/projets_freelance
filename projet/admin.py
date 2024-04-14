from django.contrib import admin
from .models import Photo, Projet, Commentaire, PartiPrenante

admin.site.register(Projet)
admin.site.register(Commentaire)
admin.site.register(PartiPrenante)
admin.site.register(Photo)
