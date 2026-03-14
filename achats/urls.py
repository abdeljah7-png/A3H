from django.urls import path
from . import views

urlpatterns = [

    path("demande/pdf/<int:id>/", views.demande_pdf, name="demande_pdf"),
    path("facture/pdf/<int:facture_id>/",
         views.facture_achat_pdf,
         name="facture_achat_pdf"),
     path(
     "fournisseur-info/<int:fournisseur_id>/",
     views.fournisseur_info,
     name="fournisseur_info"
     ),
    path("br/pdf/<int:id>/", views.br_pdf, name="br_pdf"),
     path(
     "fournisseur-info/<int:fournisseur_id>/",
     views.fournisseur_info,
     name="fournisseur_info"
     ),
    path("produit-info/<int:produit_id>/",
         views.produit_info,
         name="produit_info"),

]


    
