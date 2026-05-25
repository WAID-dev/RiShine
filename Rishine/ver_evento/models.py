from django.db import models

class Historial(models.Model):
    """
        Modelo que registra las interacciones de los usuarios
        con los eventos visualizados o consultados dentro
        de la plataforma.
    """
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='historiales')
    id_evento = models.ForeignKey('crear_evento.Evento', on_delete=models.SET_NULL, null=True, blank=True, related_name='historiales')
    # Fecha en la que se registró la interacción.
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            # Evita registrar múltiples veces el mismo evento
            # para el mismo usuario en una misma fecha
            models.UniqueConstraint(fields=['id_usuario', 'id_evento', 'fecha'], name='uq_historial_usuario_evento_fecha'),
        ]


