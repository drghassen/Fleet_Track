# models.py
from django.db import models
from django.contrib.auth.models import User

class Vehicule(models.Model):
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    immatriculation = models.CharField(max_length=20, unique=True)
    date_mise_en_service = models.DateField()
    kilometrage_actuel = models.IntegerField(default=0)
    carburant_type = models.CharField(max_length=20, choices=[
        ('essence', 'Essence'),
        ('diesel', 'Diesel'),
        ('electrique', 'Électrique')
    ])
    statut = models.CharField(max_length=20, choices=[
        ('disponible', 'Disponible'),
        ('en_mission', 'En mission'),
        ('maintenance', 'En maintenance')
    ], default='disponible')

class Chauffeur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_embauche = models.DateField()
    permis_numero = models.CharField(max_length=50)
    telephone = models.CharField(max_length=20)

class Mission(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    chauffeur = models.ForeignKey(Chauffeur, on_delete=models.CASCADE)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField(null=True, blank=True)
    lieu_depart = models.CharField(max_length=200)
    lieu_arrivee = models.CharField(max_length=200)
    statut = models.CharField(max_length=20, choices=[
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée')
    ], default='planifiee')

class PositionGPS(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    vitesse = models.FloatField(null=True, blank=True)  # km/h

class Maintenance(models.Model):
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE)
    type_maintenance = models.CharField(max_length=50, choices=[
        ('vidange', 'Vidange'),
        ('freins', 'Freins'),
        ('pneus', 'Pneus'),
        ('autre', 'Autre')
    ])
    date_maintenance = models.DateField()
    kilometrage = models.IntegerField()
    cout = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

class Notification(models.Model):
    titre = models.CharField(max_length=200)
    message = models.TextField()
    type_notification = models.CharField(max_length=20, choices=[
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('error', 'Erreur'),
        ('success', 'Succès')
    ], default='info')
    date_creation = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    utilisateur = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
