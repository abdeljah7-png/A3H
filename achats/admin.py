from django.contrib import admin, messages
from django.urls import reverse, path
from django.utils.html import format_html
from django.shortcuts import redirect

from .models import (
    Demande,
    LigneDemande,
    BonReception,
    LigneBonReception,
    FactureAchat,
    LigneFactureAchat,
)

# =====================================================
# INLINE LIGNES DEMANDE
# =====================================================

class LigneDemandeInline(admin.TabularInline):
    model = LigneDemande
    extra = 1
    fields = (
        "produit",
        "quantite",
        "prix_ht",
        "taux_rem",
        "taux_tva",
    )


# =====================================================
# ADMIN DEMANDE
# =====================================================

@admin.register(Demande)
class DemandeAdmin(admin.ModelAdmin):

    class Media:
        js = (
            "achats/br_auto_fournisseur.js",
            "achats/produit_auto_achat.js",
        )

    inlines = [LigneDemandeInline]

    list_display = (
        "numero",
        "date",
        "fournisseur",
        "statut",
        "afficher_total_ttc",
        "bouton_pdf",
    )

    search_fields = (
        "numero",
        "fournisseur__nom",
    )

    list_filter = (
        "statut",
        "date",
    )

    exclude = (
        "total_ht",
        "total_rem",
        "base_tva",
        "total_tva",
        "total_ttc",
    )

    readonly_fields = ("numero",)

    # ===============================
    # TOTAL TTC
    # ===============================
    def afficher_total_ttc(self, obj):

        total = 0

        for ligne in obj.lignes.all():

            montant_ht = ligne.quantite * ligne.prix_ht
            rem = montant_ht * (ligne.taux_rem or 0) / 100
            base = montant_ht - rem
            tva = base * (ligne.taux_tva or 0) / 100

            total += base + tva

        return f"{total:.3f} TND"

    afficher_total_ttc.short_description = "Total TTC"

    # ===============================
    # BOUTON PDF
    # ===============================
    def bouton_pdf(self, obj):

        url = reverse("demande_pdf", args=[obj.id])

        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background:#007bff;color:white;padding:4px 8px;border-radius:4px;">PDF</a>',
            url,
        )

    bouton_pdf.short_description = "PDF"


# =====================================================
# INLINE LIGNES BON RECEPTION
# =====================================================

class LigneBonReceptionInline(admin.TabularInline):
    model = LigneBonReception
    extra = 1
    fields = (
        "produit",
        "quantite",
        "prix_ht",
        "taux_rem",
        "taux_tva",
    )


# =====================================================
# ADMIN BON RECEPTION
# =====================================================

@admin.register(BonReception)
class BonReceptionAdmin(admin.ModelAdmin):

    class Media:
        js = (
            "achats/br_auto_fournisseur.js",
            "achats/produit_auto_achat.js",
        )

    inlines = [LigneBonReceptionInline]

    list_display = (
        "numero",
        "date",
        "fournisseur",
        "statut",
        "afficher_total_ttc",
        "bouton_pdf",
    )

    search_fields = (
        "numero",
        "fournisseur__nom",
    )

    list_filter = (
        "statut",
        "date",
    )

    exclude = (
        "total_ht",
        "total_rem",
        "base_tva",
        "total_tva",
        "total_ttc",
    )

    readonly_fields = ("numero",)

    # ===============================
    # TOTAL TTC
    # ===============================
    def afficher_total_ttc(self, obj):

        total = 0

        for ligne in obj.lignes.all():

            montant_ht = ligne.quantite * ligne.prix_ht
            rem = montant_ht * (ligne.taux_rem or 0) / 100
            base = montant_ht - rem
            tva = base * (ligne.taux_tva or 0) / 100

            total += base + tva

        return f"{total:.3f} TND"

    afficher_total_ttc.short_description = "Total TTC"

    # ===============================
    # BOUTON PDF
    # ===============================
    def bouton_pdf(self, obj):

        url = reverse("br_pdf", args=[obj.id])

        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background:#007bff;color:white;padding:4px 8px;border-radius:4px;">PDF</a>',
            url,
        )

    bouton_pdf.short_description = "PDF"


# =====================================================
# INLINE LIGNES FACTURE ACHAT
# =====================================================

class LigneFactureAchatInline(admin.TabularInline):
    model = LigneFactureAchat
    extra = 1


# =====================================================
# ADMIN FACTURE ACHAT
# =====================================================

@admin.register(FactureAchat)
class FactureAchatAdmin(admin.ModelAdmin):


    class Media:
        js = (
            "achats/br_auto_fournisseur.js",
            "achats/produit_auto_achat.js",
        )

    inlines = [LigneFactureAchatInline]




    list_display = (
        "numero",
        "fournisseur",
        "date",
        "statut_colore",
        "bouton_pdf",
    )

    fields = (
        "numero",
        "fournisseur",
        "mf_fournisseur",
        "adresse_fournisseur",
        "telephone_fournisseur",
        "email_fournisseur",
        "statut",
    )

    readonly_fields = (
        "numero",
    )

    # ===============================
    # STATUT COULEUR
    # ===============================
    def statut_colore(self, obj):

        couleurs = {
            "brouillon": "gray",
            "validee": "green",
            "payee": "blue",
        }

        return format_html(
            '<b style="color:{}">{}</b>',
            couleurs.get(obj.statut, "black"),
            obj.get_statut_display(),
        )

    statut_colore.short_description = "Statut"

    # ===============================
    # BOUTON PDF
    # ===============================
    def bouton_pdf(self, obj):

        url = reverse("facture_achat_pdf", args=[obj.id])

        return format_html(
            '<a class="button" href="{}" target="_blank" '
            'style="background:#007bff;color:white;padding:4px 8px;border-radius:4px;">PDF</a>',
            url,
        )

    bouton_pdf.short_description = "PDF"


# =====================================================
# ADMIN LIGNE FACTURE ACHAT
# =====================================================

@admin.register(LigneFactureAchat)
class LigneFactureAchatAdmin(admin.ModelAdmin):

    list_display = (
        "facture",
        "produit",
        "quantite",
        "prix_ht",
        "taux_rem",
        "taux_tva",
    )