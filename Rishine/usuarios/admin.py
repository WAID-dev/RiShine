from django.contrib import admin
from .models import Favorito, Guardado, Promotor, Usuario


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha_de_nacimiento", "ciudad")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "ciudad")
    list_filter = ("ciudad",)
    ordering = ("usuario__username",)
    list_select_related = ("usuario",)


@admin.register(Promotor)
class PromotorAdmin(admin.ModelAdmin):
    list_display = ("id_promotor", "usuario", "organizacion")
    search_fields = ("usuario__username", "usuario__first_name", "usuario__last_name", "organizacion")
    list_filter = ("organizacion",)
    ordering = ("organizacion", "usuario__username")
    list_select_related = ("usuario",)


@admin.register(Favorito)
class FavoritoAdmin(admin.ModelAdmin):
    list_display = ("id_favorito", "usuario", "evento")
    search_fields = ("usuario__username", "evento__titulo")
    ordering = ("-id_favorito",)
    list_select_related = ("usuario", "evento")


@admin.register(Guardado)
class GuardadoAdmin(admin.ModelAdmin):
    list_display = ("id_guardado", "usuario", "evento")
    search_fields = ("usuario__username", "evento__titulo")
    ordering = ("-id_guardado",)
    list_select_related = ("usuario", "evento")
