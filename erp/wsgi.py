import os
import django
from django.core.wsgi import get_wsgi_application
from django.contrib.auth import get_user_model

# Configuration Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "erp.settings")
django.setup()

# Création automatique du superuser si inexistant
User = get_user_model()
if not User.objects.filter(username=os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")).exists():
    User.objects.create_superuser(
        username=os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin"),
        email=os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com"),
        password=os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin123")
    )

application = get_wsgi_application()