from django.db import models
from pathlib import Path
from uuid import uuid4

class Categoria(models.Model):
    """
    Modelo utilizado para clasificar los eventos,
    facilitando la organización, filtrado y búsqueda
    de contenido dentro de la plataforma.
    """
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.nombre_categoria)

class Horario(models.Model):
    """
    Modelo que almacena los días asociados a los eventos
    """
    id_horario = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=20)

    def __str__(self):
        return str(self.dia)


# Constantes utilizadas para controlar el estado de publicación del evento.
ESTATUS_BORRADOR = 'borrador'
ESTATUS_PUBLICADO = 'publicado'

# Opciones disponibles para el campo estatus del modelo Evento.
ESTATUS_CHOICES = [
    (ESTATUS_BORRADOR, 'Borrador'),
    (ESTATUS_PUBLICADO, 'Publicado'),
]


def ruta_imagen_evento(instance, filename):
    """
    Genera una ruta única para almacenar las imágenes de los eventos,
    organizándolas por promotor y evitando nombres duplicados
    """
    extension = Path(filename).suffix.lower() or '.jpg'

    # Obtiene el ID del promotor asociado al evento
    promotor_id = getattr(instance, 'promotor_id', None) or 'sin_promotor'

    # Genera un nombre único para la imagen
    nombre_archivo = f"{uuid4().hex}{extension}"
    return f"imagen_evento/promotor_{promotor_id}/{nombre_archivo}"


class Evento(models.Model):
    """
    Modelo principal que representa los eventos publicados
    dentro de la plataforma.
    Contiene información general, fechas, ubicación,
    cupo disponible e imagen asociada
    """
    id_evento = models.AutoField(primary_key=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='evento_categoria')
    promotor = models.ForeignKey('usuarios.Promotor', on_delete=models.PROTECT, related_name='evento_promotor')
    titulo = models.CharField(max_length=50)
    descripcion = models.TextField()
    cupo = models.IntegerField()
    costo = models.IntegerField()
    direccion = models.CharField(max_length=50)
    referencias = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    horario = models.ManyToManyField(Horario, related_name='evento_horario')
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default=ESTATUS_BORRADOR)
    imagen = models.ImageField(upload_to=ruta_imagen_evento, blank=True, null=True)

    class Meta:
        constraints = [
            # Evita registrar eventos con cupo negativo
            models.CheckConstraint(condition=models.Q(cupo__gte=0), name='chk_evento_cupo_gte_0'),
            # Evita registrar costos negativos
            models.CheckConstraint(condition=models.Q(costo__gte=0), name='chk_evento_costo_gte_0'),
            # Verifica que la fecha final no sea anterior a la inicial
            models.CheckConstraint(condition=models.Q(fecha_fin__gte=models.F('fecha_inicio')), name='chk_evento_fechas_validas'),
        ]

    def __str__(self):
        return str(self.titulo)














