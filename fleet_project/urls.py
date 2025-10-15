from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView  # Pour la redirection vers le dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/fleet/')),  # Redirige la racine vers l'app
    path('fleet/', include('fleet_track.urls')),  # Inclut les URLs de votre app
]