from django.contrib import admin
from django.utils.html import format_html

from .models import Categoria, Evento, Horario


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id_categoria", "nombre_categoria")
    search_fields = ("nombre_categoria",)
    ordering = ("nombre_categoria",)


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ("id_horario", "dia")
    search_fields = ("dia",)
    ordering = ("dia",)


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = (
        "id_evento",
        "titulo",
        "categoria",
        "promotor",
        "fecha_inicio",
        "fecha_fin",
        "estatus",
    )
    list_filter = ("estatus", "categoria", "fecha_inicio", "fecha_fin")
    search_fields = ("titulo", "descripcion", "direccion", "promotor__usuario__username")
    ordering = ("-id_evento",)
    list_select_related = ("categoria", "promotor", "promotor__usuario")
    filter_horizontal = ("horario",)
    readonly_fields = ("vista_previa_imagen",)
    fieldsets = (
        (
            "Informacion del evento",
            {
                "fields": (
                    "titulo",
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
                    "horario",
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
        if obj.imagen:
            return format_html('<img src="{}" style="max-height: 160px; border-radius: 8px;" />', obj.imagen.url)
        return "Sin imagen"
