from django.http import JsonResponse
from .models import Fournisseur

def fournisseur_info(request, Fournisseur_id):
    fournisseur = Fournisseur.objects.get(id=Fournisseur_id)

    return JsonResponse({
        "mf": Fournisseur.matricule_fiscal,   # ✅ CORRIGÉ ICI
        "adresse": Fournisseur.adresse,
        "telephone": Fournisseur.telephone,
        "email": Fournisseur.email,
    })