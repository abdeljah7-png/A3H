from django.contrib import admin
from .models import Compte


@admin.register(Compte)
class CompteAdmin(admin.ModelAdmin):

    list_display = (
        "code",
        "libelle",
        "type_compte",
        "solde_initial",
        "date_creation",
    )

    search_fields = (
        "code",
        "libelle",
    )

    list_filter = (
        "type_compte",
    )
