from django.contrib import admin
from django.contrib.admin import site
import adminactions.actions as actions
from .models import *
from import_export.admin import ImportExportModelAdmin
actions.add_to_site(site)


class entidad_admin(ImportExportModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')
    list_filter = ('activo', )


class base_tabular(admin.TabularInline):
    classes = ('grp-collapse grp-open',)
    extra = 0

admin.site.register(Marca, entidad_admin)
admin.site.register(Categoria, entidad_admin)


class bodega_admin(entidad_admin):
    list_display = ('code', 'name', 'sucursal')
    list_filter = ('sucursal', 'activo')

admin.site.register(Bodega, bodega_admin)
admin.site.register(Sucursal, entidad_admin)


class producto_admin(ImportExportModelAdmin):

    fields = (('code', 'no_parte'), 'name', ('marca', 'categoria',
    'nombre_corto'), ('medida', 'modelo'), ('nauca', 'caducidad'),
        ('costo', 'precio', 'tc'), ('excento', 'almacena', 'vende',
            'compra', 'activo'))

    list_display = ('code', 'name', 'marca', 'categoria', 'precio', 'costo',
        'existencia_total')
    list_filter = ('marca', 'categoria', 'clasificacion')
    search_fields = ('code', 'name', 'no_parte', 'marca__name',
        'categoria__name')
admin.site.register(Producto, producto_admin)


class existencia_admin(admin.ModelAdmin):
    raw_id_fields = ('producto', 'bodega')
    autocomplete_lookup_fields = {
        'fk': ['producto', 'bodega'],
        }
    list_filter = ('bodega', )
    list_display = ('producto', 'existencia_disponible', 'bodega', 'ubicacion',
        'existencia_real')
    search_fields = ('producto__code', 'producto__name',
        'producto__marca__name', 'producto__categoria__name')
admin.site.register(Existencia, existencia_admin)
admin.site.register(Serie)
admin.site.register(TipoPago)


class cliente_admin(entidad_admin):
    def get_queryset(self, request):
        qs = super(cliente_admin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(vendedor=request.user)
    list_display = ('code', 'name', 'identificacion', 'telefono', 'direccion')
    fields = ('code', 'name', 'identificacion', 'telefono',
        'email', 'direccion')
    readonly_fields = ('code',)
    list_filter = ('user', 'activo')

admin.site.register(Cliente, cliente_admin)


class vendedor_admin(admin.ModelAdmin):
    list_display = ('username', 'sucursal')
    list_editable = ('sucursal', )
    list_filter = ('sucursal', )


admin.site.register(Vendedor, vendedor_admin)

admin.site.register(TipoDoc, entidad_admin)