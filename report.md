# Rapport sur le Projet FleetTrack

## Aperçu Général
FleetTrack est une application web développée avec Django pour la gestion d'une flotte de véhicules. Elle permet de suivre les véhicules, les chauffeurs, les missions, les positions GPS en temps réel, les maintenances et les notifications. L'application inclut un tableau de bord interactif avec des mises à jour en temps réel via WebSockets, des formulaires pour ajouter/modifier des données, des recherches avancées, et la génération de rapports PDF. Le projet est structuré comme une application Django standard avec une app principale `fleet_track` et un projet `fleet_project`.

Le développement a commencé avec la création d'un projet Django standard, l'ajout de modèles pour les entités métier, des vues pour l'interface utilisateur, des templates HTML, et des intégrations pour le temps réel et les rapports. Aucune authentification stricte n'est requise (login/logout supprimés). Les données initiales sont chargées via des fixtures JSON.

## Technologies Utilisées
- **Backend** : Django 5.2.7 (framework web Python pour le développement rapide d'applications web).
- **Base de Données** : SQLite3 (base de données légère intégrée, configurée par défaut dans `settings.py`).
- **Temps Réel (WebSockets)** : Django Channels 4.3.1 (pour les communications asynchrones via WebSockets), avec Redis comme couche de canaux (channels_redis 4.3.0) pour la gestion des groupes et broadcasts.
- **Serveur ASGI** : Daphne 4.2.1 (serveur ASGI pour supporter les protocoles HTTP et WebSocket).
- **Génération de PDF** : ReportLab 4.4.4 (bibliothèque pour créer des rapports PDF dynamiques).
- **Frontend** : Templates Django avec HTML/CSS/JavaScript. Utilisation de classes Bootstrap (ex. `form-control`, `form-select`) pour le styling, impliquant Bootstrap comme framework CSS (non explicitement listé mais inféré des templates).
- **Outils de Développement** :
  - Django Admin (interface d'administration intégrée).
  - Fixtures Django (pour charger des données initiales via JSON).
  - Gestion des dépendances : pip (avec virtual environment, comme indiqué par `(venv)` dans les commandes).
  - ASGI Configuration : Pour supporter les applications asynchrones.
- **Système d'Exploitation/Environnement** : Windows 11, avec VSCode comme éditeur (fichiers ouverts et visibles indiquent un workflow de développement interactif).
- **Autres** : Pathlib pour la gestion des chemins, JSON pour les fixtures et les données WebSocket.

Le projet n'utilise pas de frontend framework avancé (comme React), se concentrant sur un backend Django avec templates server-side. Pas d'API REST externe ou d'intégration cloud visible.

## Bibliothèques et Dépendances
Les dépendances sont gérées via `pip` et listées dans `requirements.txt` (généré via `pip freeze`). Voici le contenu complet :

```
asgiref==3.10.0
attrs==25.4.0
autobahn==24.4.2
Automat==25.4.16
certifi==2025.10.5
cffi==2.0.0
channels==4.3.1
channels_redis==4.3.0
charset-normalizer==3.4.4
constantly==23.10.4
cryptography==46.0.0
daphne==4.2.1
Django==5.2.7
django-channels==0.7.0
hyperlink==21.0.0
idna==3.11
incremental==24.7.2
msgpack==1.1.2
oauthlib==3.3.1
pillow==11.3.0
pyasn1==0.6.1
pyasn1_modules==0.4.2
pycparser==2.23
pyOpenSSL==25.3.0
redis==6.4.0
reportlab==4.4.4
requests==2.32.5
requests-oauthlib==2.0.0
service-identity==24.2.0
setuptools==80.9.0
six==1.17.0
sqlparse==0.5.3
Twisted==25.5.0
txaio==25.9.2
typing_extensions==4.15.0
tzdata==2025.2
urllib3==2.5.0
zope.interface==8.0.1
```

- **Clés** : Django et ses extensions (Channels, Redis), ReportLab pour PDF, Pillow pour images (si besoin), Requests pour HTTP (non utilisé directement mais présent).
- Aucune dépendance externe comme PostgreSQL ou Celery ; tout est lightweight pour le développement local.

## Structure du Projet
- **fleet_project/** : Configuration principale Django.
  - `settings.py` : Configuration (apps installées : django.contrib.*, channels, fleet_track ; DATABASES=SQLite ; CHANNEL_LAYERS=Redis ; TEMPLATES avec dirs personnalisés).
  - `asgi.py` : Routeur ASGI pour HTTP et WebSocket (inclut `fleet_track.routing`).
  - `urls.py` : URLs principales (admin, redirection vers `/fleet/`, include `fleet_track.urls`).
  - `wsgi.py` : Pour déploiement WSGI (non utilisé ici).
- **fleet_track/** : App principale.
  - `models.py` : Modèles de données.
  - `views.py` : Vues et logique métier.
  - `consumers.py` : Consommateurs WebSocket.
  - `forms.py` : Formulaires Django.
  - `admin.py` : Configuration admin.
  - `urls.py` : URLs de l'app.
  - `routing.py` : URLs WebSocket.
  - `fixtures/initial_data.json` : Données initiales (utilisateurs, chauffeurs, véhicules, missions, positions, maintenances).
  - `migrations/` : Migrations Django (0001_initial, 0002_notification).
  - `templates/` : Templates HTML (base.html, dashboard.html, vehicules/, mission/, registration/).
- **Autres** : `manage.py` (gestion Django), `db.sqlite3` (base de données), `TODO.md` (tâches complétées : suppression auth).

## Modèles et Logique
Les modèles définissent les entités métier avec relations ForeignKey et choices pour validation.

- **Vehicule** : Représente un véhicule.
  - Champs : marque, modele, immatriculation (unique), date_mise_en_service, kilometrage_actuel, carburant_type (choices: essence/diesel/electrique), statut (choices: disponible/en_mission/maintenance).
  - Logique : Suit l'état et les specs du véhicule ; utilisé comme clé pour missions, positions, maintenances.

- **Chauffeur** : Profil chauffeur lié à un User Django.
  - Champs : user (OneToOneField), date_embauche, permis_numero, telephone.
  - Logique : Extension du système auth Django ; un chauffeur par utilisateur.

- **Mission** : Affectation véhicule-chauffeur.
  - Champs : vehicule (FK), chauffeur (FK), date_debut/fin, lieu_depart/arrivee, statut (choices: planifiee/en_cours/terminee/annulee).
  - Logique : Gère les trajets ; statut mis à jour manuellement ou via vues.

- **PositionGPS** : Positions en temps réel.
  - Champs : vehicule (FK), latitude/longitude (FloatField), timestamp (auto_now_add), vitesse (optionnelle).
  - Logique : Enregistre les localisations GPS ; dernière position utilisée pour le dashboard (défaut : Paris si absente).

- **Maintenance** : Historique entretiens.
  - Champs : vehicule (FK), type_maintenance (choices: vidange/freins/pneus/autre), date_maintenance, kilometrage, cout, description.
  - Logique : Suit les coûts et dates pour planification.

- **Notification** : Alertes système.
  - Champs : titre, message, type_notification (choices: info/warning/error/success), date_creation (auto), lu, utilisateur (FK optionnel).
  - Logique : Pour broadcasts (non implémenté dans vues actuelles, mais migration présente).

Relations : OneToMany (Vehicule -> Mission/Position/Maintenance), ManyToOne (Mission -> Vehicule/Chauffeur).

## Vues et Logique des Fonctions (views.py)
Les vues gèrent les requêtes HTTP, utilisent des modèles/forms, et rendent des templates.

- **dashboard** : Affiche le tableau de bord.
  - Logique : Récupère tous les véhicules/missions en cours ; compte statuts pour graphiques (pie chart) ; dernière position GPS par véhicule (JSON pour JS, défaut Paris) ; contexte pour templates (comptes, positions).

- **vehicule_list** : Liste des véhicules avec recherche.
  - Logique : Utilise VehiculeSearchForm pour filtrer (recherche texte, statut, carburant, km min/max) via Q objects ; rend liste filtrée.

- **vehicule_detail** : Détails d'un véhicule.
  - Logique : Récupère véhicule + 10 dernières positions + maintenances (ordonnées par date) ; affiche historique.

- **mission_list** : Liste des missions avec recherche.
  - Logique : Utilise MissionSearchForm pour filtrer (recherche lieux, véhicule/chauffeur, statut, dates) ; ordonne par date_debut descendante.

- **ajouter_position** : Ajoute une position GPS.
  - Logique : Form PositionForm ; lie à véhicule ; redirige vers détail après save.

- **ajouter_vehicule** : Ajoute un véhicule.
  - Logique : Form VehiculeForm ; save et redirige vers liste.

- **ajouter_mission** : Ajoute une mission.
  - Logique : Form MissionForm ; save et redirige vers liste.

- **generate_report** : Génère PDF rapport.
  - Logique : Utilise ReportLab (SimpleDocTemplate, Paragraph, Table) ; stats générales + tableaux véhicules/missions récentes (10 dernières) ; retourne HttpResponse PDF pour téléchargement.

Autres imports : render, get_object_or_404, redirect, HttpResponse, Q pour queries, json pour sérialisation.

## Consommateurs WebSocket (consumers.py)
- **DashboardConsumer** (AsyncWebsocketConsumer) : Gère mises à jour temps réel.
  - **connect** : Ajoute au groupe 'dashboard', accepte connexion, envoie données initiales.
  - **disconnect** : Retire du groupe.
  - **dashboard_update** : Broadcast pour rafraîchir (appelé via channel_layer).
  - **send_dashboard_data** : Récupère/comptes (véhicules, chauffeurs, missions, positions, statuts) ; envoie JSON au client.
  - Méthodes statiques async : get_vehicules_count() etc., utilisent querysets optimisés (select_related pour éviter N+1 queries).
  - Logique : Fournit données live pour dashboard (ex. positions GPS mises à jour sans refresh).

## Formulaires (forms.py)
Formulaires ModelForm pour validation/crud, avec widgets Bootstrap.

- **MissionForm**, **PositionForm**, **MaintenanceForm**, **VehiculeForm** : Champs modèles + widgets (DateTimeInput, NumberInput, Select, Textarea).
- **VehiculeSearchForm**, **MissionSearchForm** : Formulaires de recherche (CharField, ChoiceField, ModelChoiceField, IntegerField/DateTimeField) ; required=False pour filtres optionnels.

## Interface Admin (admin.py)
Enregistre modèles avec ModelAdmin :
- List_display/filters/search pour chaque (ex. Vehicule : immatriculation/marque/statut ; filters sur statut/carburant).
- Logique : Interface CRUD auto-générée pour admin Django.

## URLs et Routage
- **fleet_project/urls.py** : Admin, redirection racine vers /fleet/, include fleet_track.
- **fleet_track/urls.py** : Paths pour dashboard, listes/détails véhicules/missions, ajouter, report.
- **fleet_track/routing.py** : WebSocket URL (ws/dashboard/ vers DashboardConsumer).
- **asgi.py** : ProtocolTypeRouter (HTTP -> Django, WebSocket -> AuthMiddlewareStack + URLRouter).

## Données Initiales (fixtures/initial_data.json)
JSON avec ~20 entrées : 2 users (admin/driver1), 2 chauffeurs, 7 véhicules (divers statuts/carburants), 4 missions (terminées/en_cours), 4 positions GPS, 4 maintenances. Chargé via `python manage.py loaddata initial_data.json`. Exemples : Véhicules Renault Clio (disponible), Tesla Model 3 (maintenance) ; Missions Paris-Lyon (terminée).

## Étapes Suivantes et TODO
- TODO.md complété : Suppression login/logout (décorateurs, settings, tests).
- Suggestions : Ajouter auth si besoin, intégration carte (Leaflet/OpenStreetMap pour positions), API pour mobile GPS, déploiement (Heroku/Gunicorn).

Ce rapport couvre l'ensemble du projet depuis le début (structure Django basique -> ajouts progressifs : modèles, vues, temps réel, PDF).
