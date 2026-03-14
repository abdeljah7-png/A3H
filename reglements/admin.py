from django.contrib import admin
from .models import ReglementClient, ReglementFournisseur
from django.urls import reverse
from django.utils.html import format_html


@admin.register(ReglementClient)
class ReglementClientAdmin(admin.ModelAdmin):

    list_display = ("numero", "date", "client", "montant", "mode_paiement", "imprimer_quittance")
    search_fields = ("numero", "client__nom")


    def imprimer_quittance(self, obj):
        url = reverse("quittance_client_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">Imprimer</a>',
            url
        )

    imprimer_quittance.short_description = "Quittance"



@admin.register(ReglementFournisseur)
class ReglementFournisseurAdmin(admin.ModelAdmin):

    list_display = ("numero", "date", "fournisseur", "montant", "mode_paiement", "imprimer_quittance")
    search_fields = ("numero", "fournisseur__nom")

    def imprimer_quittance(self, obj):
        url = reverse("quittance_fournisseur_pdf", args=[obj.id])
        return format_html(
            '<a class="button" href="{}" target="_blank">Imprimer</a>',
            url
        )

    imprimer_quittance.short_description="quittance"
