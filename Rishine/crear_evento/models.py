from django.db import models

class Categoria(models.Model):
    """Se utiliza para clasificar eventos,
    filtrar busquedas y mejorar las recomendaciones"""
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return str(self.nombre_categoria)

class Horario(models.Model):
    id_horario = models.AutoField(primary_key=True)
    dia = models.CharField(max_length=20)

    def __str__(self):
        return str(self.dia)


ESTATUS_BORRADOR = 'borrador'
ESTATUS_PUBLICADO = 'publicado'
ESTATUS_CHOICES = [
    (ESTATUS_BORRADOR, 'Borrador'),
    (ESTATUS_PUBLICADO, 'Publicado'),
]

class Evento(models.Model):
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
    imagen = models.ImageField(upload_to='evento_imagens', blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(cupo__gte=0), name='chk_evento_cupo_gte_0'),
            models.CheckConstraint(condition=models.Q(costo__gte=0), name='chk_evento_costo_gte_0'),
            models.CheckConstraint(condition=models.Q(fecha_fin__gte=models.F('fecha_inicio')), name='chk_evento_fechas_validas'),
        ]

    def __str__(self):
        return str(self.titulo)















