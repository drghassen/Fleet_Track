from django import forms
from .models import *

class MissionForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = ['vehicule', 'chauffeur', 'date_debut', 'date_fin', 'lieu_depart', 'lieu_arrivee']
        widgets = {
            'date_debut': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'date_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'vehicule': forms.Select(attrs={'class': 'form-control'}),
            'chauffeur': forms.Select(attrs={'class': 'form-control'}),
            'lieu_depart': forms.TextInput(attrs={'class': 'form-control'}),
            'lieu_arrivee': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PositionForm(forms.ModelForm):
    class Meta:
        model = PositionGPS
        fields = ['latitude', 'longitude', 'vitesse']
        widgets = {
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.000001',
                'placeholder': 'ex: 48.8566'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.000001',
                'placeholder': 'ex: 2.3522'
            }),
            'vitesse': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ex: 50'
            }),
        }

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['type_maintenance', 'date_maintenance', 'kilometrage', 'cout', 'description']
        widgets = {
            'date_maintenance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type_maintenance': forms.Select(attrs={'class': 'form-control'}),
            'kilometrage': forms.NumberInput(attrs={'class': 'form-control'}),
            'cout': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class VehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['marque', 'modele', 'immatriculation', 'date_mise_en_service', 'kilometrage_actuel', 'carburant_type', 'statut']
        widgets = {
            'date_mise_en_service': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'marque': forms.TextInput(attrs={'class': 'form-control'}),
            'modele': forms.TextInput(attrs={'class': 'form-control'}),
            'immatriculation': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometrage_actuel': forms.NumberInput(attrs={'class': 'form-control'}),
            'carburant_type': forms.Select(attrs={'class': 'form-control'}),
            'statut': forms.Select(attrs={'class': 'form-control'}),
        }

class VehiculeSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par marque, modèle ou immatriculation...'
        })
    )
    statut = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les statuts')] + list(Vehicule._meta.get_field('statut').choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    carburant_type = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les types')] + list(Vehicule._meta.get_field('carburant_type').choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    kilometrage_min = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Km min'
        })
    )
    kilometrage_max = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Km max'
        })
    )

class MissionSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher par lieu de départ ou d\'arrivée...'
        })
    )
    vehicule = forms.ModelChoiceField(
        required=False,
        queryset=Vehicule.objects.all(),
        empty_label="Tous les véhicules",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    chauffeur = forms.ModelChoiceField(
        required=False,
        queryset=Chauffeur.objects.all(),
        empty_label="Tous les chauffeurs",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    statut = forms.ChoiceField(
        required=False,
        choices=[('', 'Tous les statuts')] + list(Mission._meta.get_field('statut').choices),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    date_debut_min = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )
    date_debut_max = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        })
    )
