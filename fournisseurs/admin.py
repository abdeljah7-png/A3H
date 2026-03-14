from django.contrib import admin
from .models import Fournisseur


@admin.register(Fournisseur)
class fournisseurAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "matricule_fiscal",
        "telephone",
        "email",
        "date_creation",
    )
    search_fields = (
        "nom",
        "matricule_fiscal",
    )
    list_filter = ("date_creation",)
    ordering = ("nom",)