from django.db import models
from django.contrib.auth.models import User

from register.models import Client


# Create your models here.


class Livreur(models.Model):
    livreur_nom = models.CharField("Nom", max_length=50)
    livreur_prenom = models.CharField("Prénom", max_length=50)


class Trajet(models.Model):
    trajet_distance = models.FloatField(default=0)
    trajet_prix = models.FloatField(default=0)
    trajet_depart = models.DateTimeField(auto_now_add=True)
    trajet_livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE)


class Commande(models.Model):
    commande_date = models.DateTimeField(auto_now_add=True)
    commande_prix = models.FloatField(default=0)
    commande_client = models.ForeignKey(Client, on_delete=models.CASCADE)
    commande_trajet = models.ForeignKey(Trajet, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.commande_client.email} {self.commande_date}"


class Produit(models.Model):
    produit_libelle = models.CharField(max_length=128)
    produit_prix = models.FloatField(default=0.0)

    PINSA = 'PS'
    ANTIPASTI = 'AP'
    PASTA = 'PA'
    PASTALFORNO = 'PF'
    DESSERT = 'DS'
    BOISSON = 'BS'

    TYPE_PRODUIT = [
        (PINSA, 'Pinsa'),
        (ANTIPASTI, 'Antipasti'),
        (PASTA, 'Pasta'),
        (PASTALFORNO, 'Past\'al forno'),
        (DESSERT, 'Dessert'),
        (BOISSON, 'Boisson')
    ]

    produit_type = models.CharField(max_length=2, choices=TYPE_PRODUIT)

    BASIQUE = 'BQ'
    SPECIALE = 'SP'
    VEGETARIENNE = 'VG'

    TYPE_PINSA = [
        (BASIQUE, 'Basique'),
        (SPECIALE, 'Spéciale'),
        (VEGETARIENNE, 'Végétarienne')
    ]

    produit_sous_type = models.CharField(max_length=2, choices=TYPE_PINSA, null=True)
    produit_composition = models.TextField(max_length=1000, null=True)
    produit_photo = models.ImageField(upload_to="plats", blank=True, null=True)
    slug = models.SlugField(max_length=128)

    def __str__(self):
        return self.produit_libelle


class Detail(models.Model):
    detail_quantite = models.IntegerField(default=1)
    detail_notes = models.TextField(max_length=1000, null=True)
    detail_produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    detail_commande = models.ForeignKey(Commande, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.detail_produit} {self.detail_quantite} pcs"
