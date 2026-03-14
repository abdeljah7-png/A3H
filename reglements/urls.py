from django.urls import path
from . import views

urlpatterns = [

    path(
        "quittance-client/<int:pk>/",
        views.quittance_client_pdf,
        name="quittance_client_pdf"),
    path("quittance-fournisseur/<int:pk>/",
        views.quittance_fournisseur_pdf,
        name="quittance_fournisseur_pdf"),

]
