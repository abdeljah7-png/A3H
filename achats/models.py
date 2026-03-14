from django.db import models
from django.utils.timezone import now
from fournisseurs.models import Fournisseur
from produits.models import Produit
from django.db.models import Max


# =====================================================
# GENERATION NUMERO DEMANDE
# =====================================================

def generer_numero_demande():

    annee = now().year
    prefix = f"DEM-{annee}-"

    dernier = Demande.objects.filter(
        numero__startswith=prefix
    ).order_by("numero").last()

    if dernier:
        num = int(dernier.numero.split("-")[-1]) + 1
    else:
        num = 1

    return f"{prefix}{num:05d}"


# =====================================================
# DEMANDE DE PRIX
# =====================================================

class Demande(models.Model):

    STATUTS = (
        ("brouillon", "Brouillon"),
        ("envoye", "Envoyé"),
        ("accepte", "Accepté"),
        ("refuse", "Refusé"),
    )

    numero = models.CharField(max_length=30, unique=True, blank=True)

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default="brouillon"
    )

    date = models.DateField(auto_now_add=True)

    total_ht = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_rem = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    base_tva = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_tva = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_ttc = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    mf_fournisseur = models.CharField(max_length=50, blank=True)
    adresse_fournisseur = models.CharField(max_length=255, blank=True)
    telephone_fournisseur = models.CharField(max_length=20, blank=True)
    email_fournisseur = models.EmailField(blank=True)

    def __str__(self):
        return self.numero or "Demande"

    def save(self, *args, **kwargs):

        if not self.numero:
            self.numero = generer_numero_demande()

        super().save(*args, **kwargs)

    def calculer_totaux(self):

        total_ht = 0
        total_rem = 0
        base_tva = 0
        total_tva = 0
        total_ttc = 0

        for ligne in self.lignes.all():

            montant_ht = ligne.quantite * ligne.prix_ht
            montant_rem = montant_ht * (ligne.taux_rem or 0) / 100

            base = montant_ht - montant_rem
            tva = base * (ligne.taux_tva or 0) / 100

            total_ht += montant_ht
            total_rem += montant_rem
            base_tva += base
            total_tva += tva
            total_ttc += base + tva

        return {
            "total_ht": total_ht,
            "total_rem": total_rem,
            "base_tva": base_tva,
            "total_tva": total_tva,
            "total_ttc": total_ttc,
        }


class LigneDemande(models.Model):

    demande = models.ForeignKey(
        Demande,
        on_delete=models.CASCADE,
        related_name="lignes"
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT
    )

    quantite = models.DecimalField(max_digits=10, decimal_places=2)

    prix_ht = models.DecimalField("Prix Achat",max_digits=10, decimal_places=3)

    taux_rem = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    taux_tva = models.DecimalField(max_digits=4, decimal_places=2)

    def montant_ht(self):
        return self.quantite * self.prix_ht


# =====================================================
# BON RECEPTION
# =====================================================

class BonReception(models.Model):

    numero = models.CharField(max_length=20, unique=True, blank=True)

    date = models.DateField(auto_now_add=True)

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT
    )

    statut = models.CharField(
        max_length=20,
        choices=[
            ("brouillon", "Brouillon"),
            ("validee", "Validée"),
        ],
        default="brouillon"
    )

    mf_fournisseur = models.CharField(max_length=30, blank=True)
    adresse_fournisseur = models.CharField(max_length=200, blank=True)
    telephone_fournisseur = models.CharField(max_length=30, blank=True)
    email_fournisseur = models.CharField(max_length=100, blank=True)

    total_ht = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_rem = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    base_tva = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_tva = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_ttc = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    def __str__(self):
        return f"BR {self.numero}"

    def save(self, *args, **kwargs):

        if not self.numero:

            dernier = BonReception.objects.aggregate(Max("numero"))

            if dernier["numero__max"]:
                self.numero = str(int(dernier["numero__max"]) + 1)
            else:
                self.numero = "1"

        super().save(*args, **kwargs)


class LigneBonReception(models.Model):

    bon = models.ForeignKey(
        BonReception,
        related_name="lignes",
        on_delete=models.CASCADE
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT
    )

    quantite = models.DecimalField(max_digits=10, decimal_places=3)

    prix_ht = models.DecimalField("Prix Achat", max_digits=10, decimal_places=3)

    taux_rem = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    taux_tva = models.DecimalField(max_digits=5, decimal_places=2, default=19)


# =====================================================
# FACTURE ACHAT
# =====================================================

def generer_numero_facture_achat():

    annee = now().year
    prefix = f"FAC-A-{annee}-"

    derniere = FactureAchat.objects.filter(
        numero__startswith=prefix
    ).order_by("numero").last()

    if derniere:
        num = int(derniere.numero.split("-")[-1]) + 1
    else:
        num = 1

    return f"{prefix}{num:05d}"


class FactureAchat(models.Model):

    STATUTS = (
        ("brouillon", "Brouillon"),
        ("validee", "Validée"),
        ("payee", "Payée"),
    )

    numero = models.CharField(max_length=30, unique=True, blank=True)

    fournisseur = models.ForeignKey(
        Fournisseur,
        on_delete=models.PROTECT
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default="brouillon"
    )

    date = models.DateField(auto_now_add=True, editable=False)

    total_ht = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_rem = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    base_tva = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_tva = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    total_ttc = models.DecimalField(max_digits=12, decimal_places=3, default=0)

    mf_fournisseur = models.CharField(max_length=50, blank=True)
    adresse_fournisseur = models.CharField(max_length=255, blank=True)
    telephone_fournisseur = models.CharField(max_length=20, blank=True)
    email_fournisseur = models.EmailField(blank=True)

#------- calcul totaux

    def calculer_totaux(self):

        total_ht = 0
        total_rem = 0
        base_tva = 0
        total_tva = 0
        total_ttc = 0

        for ligne in self.lignes.all():

            montant_ht = ligne.quantite * ligne.prix_ht
            rem = montant_ht * (ligne.taux_rem or 0) / 100
            base = montant_ht - rem
            tva = base * (ligne.taux_tva or 0) / 100

            total_ht += montant_ht
            total_rem += rem
            base_tva += base
            total_tva += tva
            total_ttc += base + tva

        return {
            "total_ht": total_ht,
            "total_rem": total_rem,
            "base_tva": base_tva,
            "total_tva": total_tva,
            "total_ttc": total_ttc,
        }




#-----------------------




    def __str__(self):
        return self.numero or "Facture Achat"

    def save(self, *args, **kwargs):

        if not self.numero:
            self.numero = generer_numero_facture_achat()

        super().save(*args, **kwargs)


class LigneFactureAchat(models.Model):

    facture = models.ForeignKey(
        FactureAchat,
        on_delete=models.CASCADE,
        related_name="lignes"
    )

    produit = models.ForeignKey(
        Produit,
        on_delete=models.PROTECT
    )

    quantite = models.DecimalField(max_digits=10, decimal_places=2)

    prix_ht = models.DecimalField("Prix Achat", max_digits=10, decimal_places=3)

    taux_rem = models.DecimalField(max_digits=4, decimal_places=2, default=0)

    taux_tva = models.DecimalField(max_digits=4, decimal_places=2)

    def montant_ht(self):
        return self.quantite * self.prix_ht