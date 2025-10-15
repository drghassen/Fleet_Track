from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('vehicules/', views.vehicule_list, name='vehicule_list'),
    path('vehicules/<int:id>/', views.vehicule_detail, name='vehicule_detail'),
    path('vehicules/<int:vehicule_id>/position/', views.ajouter_position, name='ajouter_position'),
    path('vehicules/ajouter/', views.ajouter_vehicule, name='ajouter_vehicule'),
    path('missions/', views.mission_list, name='mission_list'),
    path('missions/ajouter/', views.ajouter_mission, name='ajouter_mission'),
    path('generate-report/', views.generate_report, name='generate_report'),
]
