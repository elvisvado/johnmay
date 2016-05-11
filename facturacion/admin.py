from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from base.admin import base_tabular
from base.models import Documento as Factura, Detalle


class DetalleFactura(base_tabular):
    model = Detalle
    fields = ('producto', 'producto_cantidad',
        'producto_precio_unitario', 'producto_descuento_unitario')

    def get_readonly_fields(self, request, obj=None):
            if obj and obj.aplicado:
                return ('producto', 'cantidad',
        'precio_unitario', 'descuento_unitario')
            else:
                return super(DetalleFactura, self).get_readonly_fields(request)

    raw_id_fields = ('producto', )
    autocomplete_lookup_fields = {
        'fk': ['producto', ],
        }
    extra = 0


class FacturaAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
            if obj and obj.aplicado:
                return ('fecha', 'tipopago',
        'fecha_vence', 'comentarios', 'cliente',
        'subtotal', 'costo', 'descuento', 'utilidad', 'iva', 'ir', 'al'
        'total', 'saldo', 'factor')
            else:
                return ('fecha', 'fecha_vence', 'subtotal', 'costo',
                    'descuento', 'utilidad', 'iva', 'ir', 'al', 'total',
                    'saldo', 'factor')

    date_hierarchy = 'fecha'
    fieldsets = (('Datos de la Factura', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('numero', 'fecha', 'tipopago'),
                            ('fecha_vence'), 'comentarios',)}),
                ('Datos del Cliente', {
                'classes': ('grp-collapse grp-open',),
                'fields': ('cliente', )}),
                ("Detalle de Productos", {"classes":
                ("placeholder detalle_set-group",), "fields": ()}),

                ('Impuestos y totales', {
                'classes': ('grp-collapse grp-open',),
                'fields': (('subtotal', 'factor'), ('descuento',
                'utilidad'), ('iva', 'ir', 'al', 'costo'),
                ('total', 'saldo'))}),
                                    )
    inlines = [DetalleFactura]
    list_display = ('numero', 'fecha', 'cliente', 'total',
        'user', 'sucursal', 'tipodoc')
    list_filter = (('fecha', DateRangeFilter), 'sucursal', 'user',
        'tipopago', 'tipodoc')
    search_fields = ('numero', )
    raw_id_fields = ('cliente', )
    autocomplete_lookup_fields = {
        'fk': ['cliente', ],
        }

    def action_aplicar(self, request, queryset):
        for d in queryset:
            d.aplicar()
    actions = [action_aplicar]
admin.site.register(Factura, FacturaAdmin)


