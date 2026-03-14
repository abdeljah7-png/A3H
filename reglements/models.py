from django.db import models
from clients.models import Client
from fournisseurs.models import Fournisseur
from comptes.models import Compte

class ReglementClient(models.Model):

 
    mode_choix=[
        ("Espece", "Espèce"),
        ("Cheque", "Cheque"),
        ("Virement" ,"Virement"),
        ("Lettre de change", "Lettre de change"),
    ]

    numero = models.CharField(max_length=20, unique=True, blank=True)
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    montant = models.DecimalField(max_digits=12, decimal_places=3)

    compte=models.ForeignKey(Compte, on_delete=models.PROTECT,  verbose_name = "0.1- comptes")

    libelle = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    mode_paiement = models.CharField(max_length=50, blank=True, choices=mode_choix)

    def save(self, *args, **kwargs):

        if not self.numero:

            dernier = ReglementClient.objects.order_by("-id").first()

            if dernier:
                num = int(dernier.numero.split("-")[1]) + 1
            else:
                num = 1

            self.numero = f"RC-{num:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero



class ReglementFournisseur(models.Model):

    
    mode_choix=[
        ("Espece", "Espèce"),
        ("Cheque", "Cheque"),
        ("Virement" ,"Virement"),
        ("Lettre de change", "Lettre de change"),
    ]

    numero = models.CharField(max_length=20, unique=True, blank=True)
    date = models.DateField()
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE)

    montant = models.DecimalField(max_digits=12, decimal_places=3)

    compte=models.ForeignKey(Compte, on_delete=models.PROTECT,  verbose_name = "0.1- comptes")

    libelle = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    mode_paiement = models.CharField(max_length=50, blank=True, choices=mode_choix)

    def save(self, *args, **kwargs):

        if not self.numero:

            dernier = ReglementFournisseur.objects.order_by("-id").first()

            if dernier:
                num = int(dernier.numero.split("-")[1]) + 1
            else:
                num = 1

            self.numero = f"RF-{num:04d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.numero