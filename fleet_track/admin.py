from django.contrib import admin
from .models import *

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ['immatriculation', 'marque', 'modele', 'kilometrage_actuel', 'statut']
    list_filter = ['statut', 'carburant_type']
    search_fields = ['immatriculation', 'marque', 'modele']

@admin.register(Chauffeur)
class ChauffeurAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_embauche', 'telephone']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'chauffeur', 'date_debut', 'statut']
    list_filter = ['statut', 'date_debut']
    search_fields = ['vehicule__immatriculation', 'chauffeur__user__username']

@admin.register(PositionGPS)
class PositionGPSAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'latitude', 'longitude', 'timestamp', 'vitesse']
    list_filter = ['timestamp']
    search_fields = ['vehicule__immatriculation']

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['vehicule', 'type_maintenance', 'date_maintenance', 'kilometrage', 'cout']
    list_filter = ['type_maintenance', 'date_maintenance']
    search_fields = ['vehicule__immatriculation']