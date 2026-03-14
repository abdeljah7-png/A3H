from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from num2words import num2words

from .models import ReglementClient, ReglementFournisseur


def montant_en_lettres(montant):

    dinars = int(montant)
    millimes = int(round((montant - dinars) * 1000))

    texte = num2words(dinars, lang="fr")

    return f"{texte} dinars {millimes:03d} millimes"


def quittance_client_pdf(request, pk):

    reglement = ReglementClient.objects.get(pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="quittance_{reglement.numero}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)

    largeur, hauteur = A4

    # ---------------------------
    # ENTETE SOCIETE
    # ---------------------------

    p.setFont("Helvetica-Bold", 14)
    p.drawString(30*mm, hauteur-30*mm, "MA SOCIETE")

    p.setFont("Helvetica", 10)
    p.drawString(30*mm, hauteur-35*mm, "Adresse : Tunis")
    p.drawString(30*mm, hauteur-40*mm, "Tel : 00 000 000")
    p.drawString(30*mm, hauteur-45*mm, "MF : 1234567/A/M/000")

    p.line(20*mm, hauteur-50*mm, 190*mm, hauteur-50*mm)

    # ---------------------------
    # TITRE
    # ---------------------------

    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(105*mm, hauteur-65*mm, "QUITTANCE CLIENT")

    # ---------------------------
    # INFOS REGLEMENT
    # ---------------------------

    p.setFont("Helvetica", 11)

    y = hauteur - 90*mm

    p.drawString(30*mm, y, f"Numero : {reglement.numero}")
    y -= 10*mm

    p.drawString(30*mm, y, f"Date : {reglement.date}")
    y -= 10*mm

    p.drawString(30*mm, y, f"Client : {reglement.client}")
    y -= 10*mm

    p.drawString(30*mm, y, f"Montant : {reglement.montant} DT")
    y -= 10*mm

    p.drawString(30*mm, y, f"Compte : {reglement.compte}")
    y -= 10*mm

    p.drawString(30*mm, y, f"Libelle : {reglement.libelle or ''}")
    y -= 15*mm

    # ---------------------------
    # MONTANT EN LETTRES
    # ---------------------------

    montant_lettres = montant_en_lettres(reglement.montant)

    p.setFont("Helvetica-Bold", 11)
    p.drawString(30*mm, y, "Arrêtée la présente quittance à la somme de :")
    y -= 10*mm

    p.drawString(30*mm, y, montant_lettres)

    # ---------------------------
    # SIGNATURE
    # ---------------------------

    p.drawString(150*mm, 40*mm, "Signature")

    p.showPage()
    p.save()

    return response

def quittance_fournisseur_pdf(request, pk):
    try:
        reglement = ReglementFournisseur.objects.get(pk=pk)
    except ReglementFournisseur.DoesNotExist:
        return HttpResponse("Règlement fournisseur non trouvé", status=404)

    # Ici tu peux générer ton PDF
    return HttpResponse("PDF test fournisseur")