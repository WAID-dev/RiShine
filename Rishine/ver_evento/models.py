from django.db import models

class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.SET_NULL, null=True, blank=True, related_name='historiales')
    id_evento = models.ForeignKey('crear_evento.Evento', on_delete=models.SET_NULL, null=True, blank=True, related_name='historiales')
    fecha = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['id_usuario', 'id_evento', 'fecha'], name='uq_historial_usuario_evento_fecha'),
        ]


