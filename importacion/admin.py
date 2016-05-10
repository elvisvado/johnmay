from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .resources import *
from .models import *


def action_integrar(modeladmin, request, queryset):
        for q in queryset:
            q.integrar()
action_integrar.short_description = "integrar registros seleccionados"


class import_admin(ImportExportModelAdmin):
    actions = [action_integrar]


class inventario_admin(import_admin):
    list_display = ('producto_codigo', 'producto_nombre', 'producto_cantidad',
        'documento_bodega', 'documento_sucursal')
    list_filter = ('documento_bodega', 'documento_sucursal')
    search_fields = ('producto_codigo', 'producto_descripcion')

admin.site.register(Inventario, inventario_admin)


class documento_admin(import_admin):
    list_display = ('documento_fecha', 'documento_numero', 'documento_tipo',
        'producto_codigo', 'producto_nombre', 'producto_cantidad')


admin.site.register(Documento, documento_admin)