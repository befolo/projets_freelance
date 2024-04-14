from django.db import models


class SpatialProjet(models.Model):
    longitude = models.CharField(max_length=128, verbose_name='longitude')
    latitude = models.CharField(max_length=128, verbose_name='latitude')

