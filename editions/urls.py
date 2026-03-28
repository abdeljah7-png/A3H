from django.urls import path
from . import views
from .views import facturation_globale
urlpatterns = [
    path('facturation-globale/', facturation_globale, name='facturation_globale'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),  # le menu ERP
    path('facturer-bons/', views.facturer_bons, name='facturer_bons'),
]