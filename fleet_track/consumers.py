import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Vehicule, Mission, Chauffeur, PositionGPS

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('dashboard', self.channel_name)
        await self.accept()

        # Send initial data
        await self.send_dashboard_data()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard('dashboard', self.channel_name)

    async def dashboard_update(self, event):
        # Handle broadcasted updates
        await self.send_dashboard_data()

    async def send_dashboard_data(self):
        # Fetch real-time data
        vehicules_count = await self.get_vehicules_count()
        chauffeurs_count = await self.get_chauffeurs_count()
        missions_count = await self.get_missions_count()
        missions_encours = await self.get_missions_encours()
        vehicules_with_positions = await self.get_vehicules_with_positions()
        vehicules_disponible = await self.get_vehicules_disponible()
        vehicules_en_mission = await self.get_vehicules_en_mission()
        vehicules_maintenance = await self.get_vehicules_maintenance()

        data = {
            'vehicules_count': vehicules_count,
            'chauffeurs_count': chauffeurs_count,
            'missions_count': missions_count,
            'missions_encours': missions_encours,
            'vehicules_with_positions': vehicules_with_positions,
            'vehicules_disponible': vehicules_disponible,
            'vehicules_en_mission': vehicules_en_mission,
            'vehicules_maintenance': vehicules_maintenance,
        }

        await self.send(text_data=json.dumps(data))

    @staticmethod
    async def get_vehicules_count():
        return Vehicule.objects.count()

    @staticmethod
    async def get_chauffeurs_count():
        return Chauffeur.objects.count()

    @staticmethod
    async def get_missions_count():
        return Mission.objects.count()

    @staticmethod
    async def get_missions_encours():
        missions = Mission.objects.filter(statut='en_cours').select_related('vehicule', 'chauffeur__user')
        return [
            {
                'vehicule': f"{mission.vehicule.marque} {mission.vehicule.modele}",
                'chauffeur': mission.chauffeur.user.get_full_name(),
                'statut': mission.statut,
            }
            for mission in missions
        ]

    @staticmethod
    async def get_vehicules_with_positions():
        vehicules = Vehicule.objects.all()
        vehicules_with_positions = []
        for vehicule in vehicules:
            latest_position = await PositionGPS.objects.filter(vehicule=vehicule).order_by('-timestamp').afirst()
            vehicules_with_positions.append({
                'vehicule': {
                    'id': vehicule.id,
                    'marque': vehicule.marque,
                    'modele': vehicule.modele,
                    'immatriculation': vehicule.immatriculation,
                    'statut': vehicule.statut,
                },
                'position': {
                    'latitude': latest_position.latitude if latest_position else 48.8566,  # Default Paris
                    'longitude': latest_position.longitude if latest_position else 2.3522,
                } if latest_position else None
            })
        return vehicules_with_positions

    @staticmethod
    async def get_vehicules_disponible():
        return Vehicule.objects.filter(statut='disponible').count()

    @staticmethod
    async def get_vehicules_en_mission():
        return Vehicule.objects.filter(statut='en_mission').count()

    @staticmethod
    async def get_vehicules_maintenance():
        return Vehicule.objects.filter(statut='maintenance').count()
