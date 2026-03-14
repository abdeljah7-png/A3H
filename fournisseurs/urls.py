from django.urls import path
from .views import fournisseur_info

urlpatterns = [
    path("fournisseur-info/<int:fournisseur_id>/", fournisseur_info, name="fournisseur_info"),
]