from django.db import models
from projet.models import Projet


class SpatialProjet(models.Model):
    leprojet = models.OneToOneField(Projet, on_delete=models.CASCADE, unique=True, default=None)
    longitude = models.CharField(max_length=128, verbose_name='longitude')
    latitude = models.CharField(max_length=128, verbose_name='latitude')

    def __str__(self):
        return f'{self.leprojet.titre} : [{self.latitude}, {self.longitude}]'


