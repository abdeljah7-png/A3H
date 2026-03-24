from django.urls import path
from .views import client_info

urlpatterns = [
    path("client-info/<int:client_id>/", client_info, name="client_info"),
]