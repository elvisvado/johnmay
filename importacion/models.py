from django.db import models
from base.base import base_documento, base_producto, base_cliente
from base.api import *
from base.models import Existencia


class Inventario(base_documento, base_producto):
    ubicacion = models.CharField(max_length=20, null=True, blank=True)

    def integrar(self):
        p = self.get_producto()
        pb, create = Existencia.objects.get_or_create(
            producto=p, bodega=self.get_bodega())
        pb.existencia_real = self.producto_cantidad
        pb.ubicacion = self.ubicacion
        pb.save()
        self.delete()
        return p

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "inventario inicial"


class Documento(base_documento, base_producto, base_cliente):

    def integrar(self):
        if get_detalle(self):
            self.delete()

    def __unicode__(self):
        return "Documento %s %s" % (str(self.documento_numero),
            self.producto_codigo)
