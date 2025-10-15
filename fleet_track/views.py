from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from django.db.models import Q
import json
from .models import *
from .forms import *

def dashboard(request):
    vehicules = Vehicule.objects.all()
    missions_encours = Mission.objects.filter(statut='en_cours')

    # Calculate vehicle status counts for pie chart
    vehicules_disponible = vehicules.filter(statut='disponible').count()
    vehicules_en_mission = vehicules.filter(statut='en_mission').count()
    vehicules_maintenance = vehicules.filter(statut='maintenance').count()

    # Get latest positions for all vehicles
    vehicules_with_positions = []
    for vehicule in vehicules:
        latest_position = PositionGPS.objects.filter(vehicule=vehicule).order_by('-timestamp').first()
        vehicules_with_positions.append({
            'vehicule': vehicule,
            'position': latest_position
        })

    # Prepare JSON data for JavaScript
    vehicules_with_positions_json = json.dumps([
        {
            'vehicule': {
                'id': item['vehicule'].id,
                'marque': item['vehicule'].marque,
                'modele': item['vehicule'].modele,
                'immatriculation': item['vehicule'].immatriculation,
                'statut': item['vehicule'].statut
            },
            'position': {
                'latitude': item['position'].latitude if item['position'] else 48.8566,
                'longitude': item['position'].longitude if item['position'] else 2.3522
            } if item['position'] else None
        }
        for item in vehicules_with_positions
    ])

    context = {
        'vehicules': vehicules,
        'missions_encours': missions_encours,
        'vehicules_count': vehicules.count(),
        'chauffeurs_count': Chauffeur.objects.count(),
        'missions_count': Mission.objects.count(),
        'vehicules_disponible': vehicules_disponible,
        'vehicules_en_mission': vehicules_en_mission,
        'vehicules_maintenance': vehicules_maintenance,
        'vehicules_with_positions': vehicules_with_positions,
        'vehicules_with_positions_json': vehicules_with_positions_json,
    }
    return render(request, 'dashboard.html', context)

def vehicule_list(request):
    vehicules = Vehicule.objects.all()
    search_form = VehiculeSearchForm(request.GET)
    
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        statut = search_form.cleaned_data.get('statut')
        carburant_type = search_form.cleaned_data.get('carburant_type')
        kilometrage_min = search_form.cleaned_data.get('kilometrage_min')
        kilometrage_max = search_form.cleaned_data.get('kilometrage_max')
        
        if search:
            vehicules = vehicules.filter(
                Q(marque__icontains=search) |
                Q(modele__icontains=search) |
                Q(immatriculation__icontains=search)
            )
        
        if statut:
            vehicules = vehicules.filter(statut=statut)
        
        if carburant_type:
            vehicules = vehicules.filter(carburant_type=carburant_type)
        
        if kilometrage_min is not None:
            vehicules = vehicules.filter(kilometrage_actuel__gte=kilometrage_min)
        
        if kilometrage_max is not None:
            vehicules = vehicules.filter(kilometrage_actuel__lte=kilometrage_max)
    
    return render(request, 'vehicules/list.html', {
        'vehicules': vehicules,
        'search_form': search_form
    })

def vehicule_detail(request, id):
    vehicule = get_object_or_404(Vehicule, id=id)
    positions = PositionGPS.objects.filter(vehicule=vehicule).order_by('-timestamp')[:10]
    maintenances = Maintenance.objects.filter(vehicule=vehicule).order_by('-date_maintenance')
    
    return render(request, 'vehicules/detail.html', {
        'vehicule': vehicule,
        'positions': positions,
        'maintenances': maintenances
    })

def mission_list(request):
    missions = Mission.objects.all().order_by('-date_debut')
    search_form = MissionSearchForm(request.GET)
    
    if search_form.is_valid():
        search = search_form.cleaned_data.get('search')
        vehicule = search_form.cleaned_data.get('vehicule')
        chauffeur = search_form.cleaned_data.get('chauffeur')
        statut = search_form.cleaned_data.get('statut')
        date_debut_min = search_form.cleaned_data.get('date_debut_min')
        date_debut_max = search_form.cleaned_data.get('date_debut_max')
        
        if search:
            missions = missions.filter(
                Q(lieu_depart__icontains=search) |
                Q(lieu_arrivee__icontains=search)
            )
        
        if vehicule:
            missions = missions.filter(vehicule=vehicule)
        
        if chauffeur:
            missions = missions.filter(chauffeur=chauffeur)
        
        if statut:
            missions = missions.filter(statut=statut)
        
        if date_debut_min:
            missions = missions.filter(date_debut__gte=date_debut_min)
        
        if date_debut_max:
            missions = missions.filter(date_debut__lte=date_debut_max)
    
    return render(request, 'mission/list.html', {
        'missions': missions,
        'search_form': search_form
    })

def ajouter_position(request, vehicule_id):
    vehicule = get_object_or_404(Vehicule, id=vehicule_id)
    
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save(commit=False)
            position.vehicule = vehicule
            position.save()
            return redirect('vehicule_detail', id=vehicule_id)
    else:
        form = PositionForm()
    
    return render(request, 'vehicules/ajouter_position.html', {
        'form': form,
        'vehicule': vehicule
    })

# Vues supplémentaires pour compléter le MVP
def ajouter_vehicule(request):
    if request.method == 'POST':
        form = VehiculeForm(request.POST)
        if form.is_valid():
            vehicule = form.save()
            return redirect('vehicule_list')
    else:
        form = VehiculeForm()

    return render(request, 'vehicules/ajouter_vehicule.html', {'form': form})

def ajouter_mission(request):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('mission_list')
    else:
        form = MissionForm()

    return render(request, 'mission/ajouter_mission.html', {'form': form})

def generate_report(request):
    # Créer un buffer pour le PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Titre
    title = Paragraph("Rapport FleetTrack", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Statistiques générales
    vehicules_count = Vehicule.objects.count()
    chauffeurs_count = Chauffeur.objects.count()
    missions_count = Mission.objects.count()

    stats_text = f"""
    Statistiques générales:<br/>
    - Nombre de véhicules: {vehicules_count}<br/>
    - Nombre de chauffeurs: {chauffeurs_count}<br/>
    - Nombre de missions: {missions_count}
    """
    story.append(Paragraph(stats_text, styles['Normal']))
    story.append(Spacer(1, 12))

    # Tableau des véhicules
    vehicules = Vehicule.objects.all()
    vehicule_data = [['Marque', 'Modèle', 'Immatriculation', 'Statut']]
    for v in vehicules:
        vehicule_data.append([v.marque, v.modele, v.immatriculation, v.statut])

    vehicule_table = Table(vehicule_data)
    vehicule_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(vehicule_table)
    story.append(Spacer(1, 12))

    # Tableau des missions récentes
    missions = Mission.objects.all().order_by('-date_debut')[:10]
    mission_data = [['Véhicule', 'Chauffeur', 'Départ', 'Arrivée', 'Statut']]
    for m in missions:
        mission_data.append([
            f"{m.vehicule.marque} {m.vehicule.modele}",
            m.chauffeur.user.get_full_name(),
            m.lieu_depart,
            m.lieu_arrivee,
            m.statut
        ])

    mission_table = Table(mission_data)
    mission_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(mission_table)

    # Construire le PDF
    doc.build(story)
    buffer.seek(0)

    # Retourner le PDF comme réponse HTTP
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fleettrack_report.pdf"'
    return response
