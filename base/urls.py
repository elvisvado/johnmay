# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('base.views',
    url(r'^datoscliente/$', 'datos_cliente', name='datos_cliente'),
)