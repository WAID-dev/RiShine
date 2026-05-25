from django.db import models
from django.conf import settings


class Usuario(models.Model):
    """
    Modelo que almacena información complementaria del usuario autenticado,
    permitiendo mantener datos adicionales no incluidos en el modelo base
    de autenticación de Django
    """
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='usuario',
    )
    fecha_de_nacimiento = models.DateField()
    ciudad = models.CharField(max_length=50)

    def __str__(self):
        return f"Usuario<{self.usuario_id}>"

class Promotor(models.Model):
    """
    Modelo que representa a los usuarios con permisos de promotor.
    Permite almacenar información adicional necesaria para la gestión
    y publicación de eventos dentro de la plataforma
    """
    id_promotor = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='promotor'
    )
    organizacion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=12)

    def __str__(self):
        return f"Promotor<{self.usuario_id}>"


class Favorito(models.Model):
    """
    Modelo que registra los eventos marcados como favoritos
    por los usuarios para facilitar su acceso posterior
    """
    id_favorito = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favoritos')
    evento = models.ForeignKey('crear_evento.Evento', on_delete=models.CASCADE, related_name='favoritos')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'evento'], name='uq_favorito_usuario_evento'),
        ]

    def __str__(self):
        return f"Favorito<u:{self.usuario_id}, e:{self.evento_id}>"

class Guardado(models.Model):
    """
    Modelo que almacena los eventos guardados por el usuario
    para consultarlos posteriormente
    """
    id_guardado = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardados')
    evento = models.ForeignKey('crear_evento.Evento', on_delete=models.CASCADE, related_name='guardados')

    class Meta:
        # Evita duplicados un usuario solo puede guardar un mismo evento una vez
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'evento'], name='uq_guardado_usuario_evento'),
        ]

    def __str__(self):
        return f"Guardado<u:{self.usuario_id}, e:{self.evento_id}>"
