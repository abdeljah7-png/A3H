from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import cm
from django.utils.dateparse import parse_date
from .models import Client
from reglements.models import MouvementCompte  # Même modèle pour mouvements
from core.models import Societe
from django.shortcuts import render, get_object_or_404
from .models import Client
from django.utils.timezone import now
from ventes.models import BonLivraison,Facture # adapte si besoin
from reglements.models import ReglementClient



def client_info(request, client_id):
    client = Client.objects.get(id=client_id)

    return JsonResponse({
        "mf": client.matricule_fiscal,   # ✅ CORRIGÉ ICI
        "adresse": client.adresse,
        "telephone": client.telephone,
        "email": client.email,
    })

#--------   Relevé client

# ------------------- UTILITAIRE -------------------
def calcul_releve_client(client):
  

    bons = BonLivraison.objects.filter(client=client)
    reglements = ReglementClient.objects.filter(client=client)

    mouvements = []

    # 📄 Bons = DEBIT
    for b in bons:
        mouvements.append({
            "date": b.date,
            "libelle": f"Bon n°{b.numero}",
            "debit": b.total_ttc,
            "credit": 0
        })

    # 💰 Règlements = CREDIT
    for r in reglements:
        mouvements.append({
            "date": r.date,
            "libelle": f"Règlement n°{r.numero}",
            "debit": 0,
            "credit": r.montant
        })

    # 🔥 TRI PAR DATE
    mouvements.sort(key=lambda x: x["date"])

    # 🔥 CALCUL SOLDE
    solde = 0
    lignes = []

    for m in mouvements:
        solde += m["debit"] - m["credit"]

        m["solde"] = solde
        lignes.append(m)

    return lignes, solde

def releve_client(request, client_id):
   
    client = get_object_or_404(Client, id=client_id)

    lignes, solde = calcul_releve_client(client)

    return render(request, "clients/releve_client.html", {
        "client": client,
        "lignes": lignes,
        "solde": solde,
        "now": now()
    })

