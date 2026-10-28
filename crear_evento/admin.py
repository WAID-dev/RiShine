from django.contrib import admin
from django.utils.html import format_html

from .models import Categoria, Evento


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Categoria
    dentro del panel administrativo
    """
    # Columnas visibles en la lista del administrador
    list_display = ("id_categoria", "nombre_categoria")
    # Permite buscar categorías por nombre
    search_fields = ("nombre_categoria",)
    # Ordena las categorías alfabéticamente
    ordering = ("nombre_categoria",)



@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    """
    Configuración personalizada del modelo Evento
    dentro del panel administrativo
    """
    # Define las columnas visibles
    # en la lista de eventos
    list_display = (
        "id_evento",
        "nombre_evento",
        "categoria",
        "promotor",
        "fecha_inicio",
        "fecha_fin",
        "estatus",
    )

    # Agrega filtros laterales para facilitar búsquedas
    list_filter = ("estatus", "categoria", "fecha_inicio", "fecha_fin")

    # Habilita búsqueda por distintos campos
    search_fields = ("nombre_evento", "descripcion", "direccion", "promotor__usuario__username")

    # Ordena los eventos desde el más reciente
    ordering = ("-id_evento",)

    # Optimiza consultas relacionadas dentro del panel administrativo
    list_select_related = ("categoria", "promotor", "promotor__usuario")

    # Campo de solo lectura utilizado para mostrar la vista previa de la imagen
    readonly_fields = ("vista_previa_imagen",)

    # Organiza visualmente los campos
    fieldsets = (
        (
            "Informacion del evento",
            {
                "fields": (
                    "nombre_evento",
                    "descripcion",
                    "categoria",
                    "promotor",
                    "cupo",
                    "costo",
                    "estatus",
                )
            },
        ),
        (
            "Direccion y fechas",
            {
                "fields": (
                    "direccion",
                    "referencias",
                    "fecha_inicio",
                    "fecha_fin",
                )
            },
        ),
        (
            "Imagen",
            {
                "fields": ("imagen", "vista_previa_imagen"),
            },
        ),
    )

    @admin.display(description="Vista previa")
    def vista_previa_imagen(self, obj):
        """
        Muestra una vista previa de la imagen
        del evento dentro del panel administrativo.
        """
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 160px; border-radius: 8px;" />', obj.imagen.url)
        return "Sin imagen"
