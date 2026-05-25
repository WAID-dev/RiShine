from django.contrib import admin
from .models import Favorito, Guardado, Promotor, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Usuario
    dentro del panel administrativo
    """

    # Columnas visibles en el administrador
    list_display = ("id", "usuario", "fecha_de_nacimiento", "ciudad")

    # Campos habilitados para búsqueda
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "ciudad")

    # Filtros laterales disponibles
    list_filter = ("ciudad",)

    # Ordena usuarios por nombre de usuario
    ordering = ("usuario__username",)

    # Optimiza consultas relacionadas
    list_select_related = ("usuario",)


@admin.register(Promotor)
class PromotorAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Promotor
    dentro del panel administrativo.
    """

    list_display = ("id_promotor", "usuario", "organizacion")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "organizacion")
    list_filter = ("organizacion",)
    ordering = ("organizacion", "usuario__username")
    # Optimiza acceso a la relación usuario
    list_select_related = ("usuario",)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Favorito
    dentro del panel administrativo.
    """
    list_display = ("id_favorito", "usuario", "evento")
    search_fields = ("usuario__username", "evento__titulo")
    ordering = ("-id_favorito",)
    # Optimiza consultas relacionadas
    list_select_related = ("usuario", "evento")


@admin.register(Guardado)
class GuardadoAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Guardado
    dentro del panel administrativo.
    """
    list_display = ("id_guardado", "usuario", "evento")
    search_fields = ("usuario__username", "evento__titulo")
    ordering = ("-id_guardado",)
    # Optimiza consultas relacionadas
    list_select_related = ("usuario", "evento")
