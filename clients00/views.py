from django.http import JsonResponse
from .models import Client

def client_info(request, client_id):
    client = Client.objects.get(id=client_id)

    return JsonResponse({
        "mf": client.matricule_fiscal,   # ✅ CORRIGÉ ICI
        "adresse": client.adresse,
        "telephone": client.telephone,
        "email": client.email,
    })