from django.db import models
from base.models import Bodega, Sucursal
from django.contrib.auth.models import User


class Documento(models.Model):
    fecha = models.DateTimeField()
    user = models.ForeignKey(User)
    sucursal = models.ForeignKey(Sucursal)
    bodega = models.ForeignKey(Bodega)
    comentarios = models.CharField(max_length=75)


class Detalle(models.Model):
    documento = models.ForeignKey(Documento)

