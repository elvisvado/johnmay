from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *


class producto_admin(ImportExportModelAdmin):
    list_display = ('codigo', 'descripcion', 'marca', 'rack', 'columna', 'fila',
        'costo', 'existencia', 'conteo1', 'conteo2', 'conteo3',
        'con_diferencia')
    list_filter = ('bodega', 'rack', 'con_diferencia')
    list_editable = ('conteo1', 'conteo2', 'conteo3')
    actions = ['action_evaluar']

    def action_evaluar(self, request, queryset):
        for obj in queryset:
            obj.evaluar()

admin.site.register(Producto, producto_admin)