from django.db import models
from django.conf import settings


class Usuario(models.Model):
    """Permite tener un registro de todos los usuarios que han iniciado sesión
    almacenando informacion no invasiva"""
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
    """Todos los promotores son usuarios pero con funcionalidades extras
    como publicar eventos, requiere informacion mas veridica"""
    id_promotor = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='promotor'
    )
    organizacion = models.CharField(max_length=50)

    def __str__(self):
        return f"Promotor<{self.usuario_id}>"


class Favorito(models.Model):
    """Guarda los eventos favoritos seleccioandos por el usuario"""
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
    """Catalogo de eventos creado por el usuario"""
    id_guardado = models.BigAutoField(primary_key=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guardados')
    evento = models.ForeignKey('crear_evento.Evento', on_delete=models.CASCADE, related_name='guardados')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuario', 'evento'], name='uq_guardado_usuario_evento'),
        ]

    def __str__(self):
        return f"Guardado<u:{self.usuario_id}, e:{self.evento_id}>"
