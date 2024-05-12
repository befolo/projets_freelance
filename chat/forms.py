from django import forms
from .models import GroupeChat, Message
from projet.models import PartiPrenante, Projet


class ProjetChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.titre


class GroupeChatForm(forms.ModelForm):
    projet = ProjetChoiceField(queryset=None)

    class Meta:
        model = GroupeChat
        fields = ['titre', 'sujet', 'projet']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(GroupeChatForm, self).__init__(*args, **kwargs)
        # Filtrer les projets accessibles à l'utilisateur
        if self.user:
            projects = PartiPrenante.objects.filter(lepartiprenant=self.user).values_list('projet', flat=True)
            self.fields['projet'].queryset = Projet.objects.filter(pk__in=projects).distinct()
        else:
            self.fields['projet'].queryset = Projet.objects.none()


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['contenu', 'file']
