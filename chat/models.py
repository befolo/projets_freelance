from django.db import models
from django.conf import settings
from projet.models import Projet


class GroupeChat(models.Model):
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    createur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    titre = models.CharField(max_length=100, blank=False, verbose_name='titre')
    sujet = models.CharField(max_length=700, blank=True, null=True, verbose_name='sujet')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Groupe de Chat pour le projet {self.projet.titre}'


class Message(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    groupechat = models.ForeignKey(GroupeChat, on_delete=models.CASCADE, related_name='messages')
    contenu = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    date_envoi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message de {self.auteur.username} dans {self.groupechat}'
