from django.db import models
import time
import os
from .user import User
from django.contrib.postgres.fields import ArrayField



def logo_directory_path(instance, filename):
    date = time.strftime("%Y%m%d%H%M%S")
    ext = os.path.splitext(filename)[1]
    return f'logo/{date}{ext}'

class Parametre(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nom_attelier = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    numWhtsapp = models.CharField(max_length=120, null=True, blank=True)
    pays = models.CharField(max_length=120, blank=True, null=True)
    ville = models.CharField(max_length=120, blank=True, null=True)
    profile_image =  models.ImageField(upload_to=logo_directory_path, default="tayeur/tayeur-logo.png",null=True, blank=True)
    mesure_title = ArrayField(models.CharField(max_length=200), blank=True,null=True)



class ParametreImage(models.Model):
    parametre = models.ForeignKey(Parametre, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='tayeurImages/', null=True, blank=True)

