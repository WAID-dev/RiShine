from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


def almacen_privado():
    """Carpeta fuera de MEDIA: los archivos de aquí no tienen URL pública."""
    return FileSystemStorage(location=settings.BASE_DIR / 'archivos_privados')


class Perfil(models.Model):
    """Datos extra del usuario que el modelo de usuario de Django no trae."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='perfil'
    )
    fecha_nacimiento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.usuario.get_username()


class Promotor(models.Model):
    """Un usuario que publica eventos. El INE se guarda en almacenamiento privado."""
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='promotor'
    )
    organizacion = models.CharField(max_length=50)
    ine = models.FileField(upload_to='ine/', storage=almacen_privado)
    ine_verificado = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.organizacion} ({self.usuario.get_username()})'
