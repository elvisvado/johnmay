# -*- coding: utf-8 -*-
from import_export import resources
from .models import *


#class factura_resource(resources.ModelResource):
    #class Meta:
        #model = Factura
        #fields = ('id', 'fecha_importacion', 'fecha', 'numero', 'sucursal',
            #'bodega', 'tipopago', 'vendedor', 'cliente_codigo',
            #'cliente_nombre', 'cliente_identificacion', 'cliente_direccion',
            #'cliente_telefono', 'cliente_email', 'factura_costo',
            #'factura_saldo', 'factura_subtotal', 'factura_descuento',
            #'factura_impuesto', 'factura_retencion', 'factura_total',
            #'producto_codigo', 'producto_nombre', 'producto_marca',
            #'producto_categoria', 'producto_cantidad', 'producto_costo',
            #'producto_precio', 'producto_descuento')
        #export_order = fields