from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Favorito, Guardado, Promotor, Usuario


# Register your models here.
@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    """
    Configuración del modelo Usuario
    dentro del panel administrativo
    """

    fieldsets = UserAdmin.fieldsets + (
        ('Datos extra', {'fields': ('fecha_de_nacimiento', 'ciudad', 'foto')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos extra', {'fields': ('email', 'fecha_de_nacimiento', 'ciudad', 'foto')}),
    )

@admin.register(Promotor)
class PromotorAdmin(admin.ModelAdmin):
    """
    Configuración del modelo Promotor
    dentro del panel administrativo.
    """

    list_display = ("id_promotor", "usuario", "organizacion")
    search_fields = ("usuario__email", "usuario__username", "usuario__first_name", "usuario__last_name", "organizacion")
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
    search_fields = ("usuario__username", "evento__nombre_evento")
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
















