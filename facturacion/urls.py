# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('facturacion.views',
    url(r'^$', 'facturacion', name='facturacion'),
    url(r'^datos_producto/$', 'datos_producto', name='datos_producto'),
    url(r'^buscar_cliente/$', 'autocomplete_cliente',
        name='autocomplete_cliente'),
    url(r'^buscar_producto/$', 'autocomplete_producto',
        name='autocomplete_producto'),
    url(r'^datos_cliente/$', 'datos_cliente', name='datos_cliente'),
    url(r'^existencias_producto/$', 'existencias_producto',
        name='existencias_producto'),
)