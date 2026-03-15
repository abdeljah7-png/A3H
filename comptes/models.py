from django.db import models


class Compte(models.Model):

    TYPE_COMPTE = [
        ("CAISSE", "Caisse"),
        ("BANQUE", "Banque"),
    ]

    code = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Code"
    )

    libelle = models.CharField(
        max_length=100,
        verbose_name="Libellé"
    )

    type_compte = models.CharField(
        max_length=10,
        choices=TYPE_COMPTE,
        verbose_name="Type"
    )

    solde_initial = models.DecimalField(
        max_digits=12,
        decimal_places=3,
        default=0,
        verbose_name="Solde initial"
    )

    date_creation = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.code} - {self.libelle}"



from django.db import models
from django.db.models import Sum

class MouvementCompte(models.Model):
    TYPE_MOUVEMENT = [
        ("ENTREE", "Entrée"),
        ("SORTIE", "Sortie"),
    ]

    compte = models.ForeignKey('Compte', on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    type_mouvement = models.CharField(max_length=10, choices=TYPE_MOUVEMENT)
    reference = models.CharField(max_length=50)  # ex: RC-0001 ou RF-0001
    montant = models.DecimalField(max_digits=12, decimal_places=3)
    description = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.compte.code} | {self.type_mouvement} | {self.montant} | {self.reference}"

# Ajouter cette méthode à ton modèle Compte existant
def solde_actuel(self):
    entrees = self.mouvementcompte_set.filter(type_mouvement="ENTREE").aggregate(total=Sum('montant'))['total'] or 0
    sorties = self







