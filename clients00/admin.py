from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
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
        "telephone",
        "email",
    )
    list_filter = ("date_creation",)
    ordering = ("nom",)