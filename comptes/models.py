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

