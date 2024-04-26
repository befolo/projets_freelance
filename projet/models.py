from django.db import models
from django.conf import settings
from PIL import Image


class Photo(models.Model):
    image = models.ImageField()
    caption = models.CharField(max_length=128, blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()


class Projet(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    lescommentaire = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Commentaire',
                                         related_name='commentaires')
    partiprenantes = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PartiPrenante',
                                            related_name='parti_prenantes')
    titre = models.CharField(max_length=128, verbose_name='titre')
    description = models.CharField(max_length=5000, verbose_name='description')
    descrip_reduit = models.CharField(max_length=350, null=True)
    financement = models.CharField(max_length=100, verbose_name='Financement')
    entreprise = models.CharField(max_length=100, verbose_name='Entreprise')
    delais_execution = models.CharField(max_length=50, verbose_name='Delais d\'execution')
    date_created = models.DateTimeField(auto_now_add=True)

    def _get_descrip_reduit(self):
        if len(self.description) > 325:
            return self.description[:325]
        else:
            return self.description

    def __str__(self):
        return f'{self.titre}'

    def save(self, *args, **kwargs):
        self.descrip_reduit = self._get_descrip_reduit()
        super().save(*args, **kwargs)


class Commentaire(models.Model):
    commentateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    leprojet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    photo = models.OneToOneField(Photo, on_delete=models.CASCADE)
    contenu = models.CharField(max_length=5000, blank=False, verbose_name='contenu')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.commentateur.username} \n{self.leprojet.titre}'


# comment creer des formulaire avec des relations

class PartiPrenante(models.Model):
    AUTORITE_CONTRACTANTE = 'AUTORITE_CONTRACTANTE'
    MAITRE_D_OUVRAGE = 'MAITRE_D_OUVRAGE'
    CHEF_DU_MARCHE = 'CHEF_DU_MARCHE'
    INGENIEUR_DU_MARCHE = 'INGENIEUR_DU_MARCHE'
    MAITRISE_D_OEUVRE = 'MAITRISE_D_OEUVRE'

    ROLE_CHOICES = (
        (AUTORITE_CONTRACTANTE, 'Autorite Contractante'),
        (MAITRE_D_OUVRAGE, 'Maitre d\'Ouvrage'),
        (CHEF_DU_MARCHE, 'Chef du Marché'),
        (INGENIEUR_DU_MARCHE, 'Ingenieur du marché'),
        (MAITRISE_D_OEUVRE, 'Maitrise d\'Oeuvre'),
    )
    lepartiprenant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, verbose_name='rôle')
    specifications = models.CharField(max_length=100, verbose_name='specifications du rôle')

    def __str__(self):
        return f'{self.lepartiprenant.username} : {self.role} - {self.projet.titre}'
