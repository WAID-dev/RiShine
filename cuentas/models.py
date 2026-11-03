from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


def almacen_privado():
    """Carpeta fuera de MEDIA: los archivos de aquí no tienen URL pública."""
    return FileSystemStorage(location=settings.BASE_DIR / 'archivos_privados')

