from django import forms

from . import models


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image', 'caption']  # Excluez 'uploader' et 'date_created'


class CommentaireForm(forms.ModelForm):
    contenu = forms.CharField(widget=forms.Textarea)  # Utilisez forms.Textarea pour le champ 'contenu'

    class Meta:
        model = models.Commentaire
        fields = ['contenu']  # Excluez 'commentateur', 'leprojet', 'photo', 'date_created'
