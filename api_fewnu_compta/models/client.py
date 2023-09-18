from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from .user import User



class Customer(models.Model):
    FEMME = "femme"
    HOMME = "homme"
    SEXE = (
        (FEMME, 'femme'),
        (HOMME, 'homme')
    )
    # date = models.DateTimeField(default=timezone.now)
    nom_complet = models.CharField(max_length=250)
    telephone = models.CharField(max_length=30)
    adresse = models.CharField(max_length=250, null=True, blank=True)
    pays = models.CharField(max_length=255, null=True, blank=True)
    Ville = models.CharField(max_length=255,null=True, blank=True)
    sexe = models.CharField(max_length=10,choices=SEXE,default=FEMME,)
    cou=models.IntegerField(null=True, blank=True)
    epaule=models.IntegerField(null=True, blank=True)
    longueur_boubou=models.IntegerField(null=True, blank=True)
    longueur_manche=models.IntegerField(null=True, blank=True)
    cuisse=models.IntegerField(null=True, blank=True)
    longueur_pantalon=models.IntegerField(null=True, blank=True)
    hanche=models.IntegerField(null=True, blank=True)
    ceinture=models.IntegerField(null=True, blank=True)
    tour_bras=models.IntegerField(null=True, blank=True)
    poitrine=models.IntegerField(null=True, blank=True)
    taille=models.IntegerField(null=True, blank=True)
    longueur_robe=models.IntegerField(null=True, blank=True)
    longueur_poitrine=models.IntegerField(null=True, blank=True)
    bretelle=models.IntegerField(null=True, blank=True)
    longueur_jupe=models.IntegerField(null=True, blank=True)
    longueur_haut=models.IntegerField(null=True, blank=True)
    blouse=models.IntegerField(null=True, blank=True)
    autre=models.IntegerField(null=True, blank=True)
    mesure_client = ArrayField(models.JSONField(), null=True, blank=True)
    # created_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    archived = models.BooleanField(default=False)



    class Meta:
        """
        For models split into separate files, specify table name and app name.
        See https://code.djangoproject.com/wiki/CookBookSplitModelsToFiles
        """
        db_table = "api_fewnu_compta_client"
        app_label = "api_fewnu_compta"

    def __str__(self):
        return self.nom_complet