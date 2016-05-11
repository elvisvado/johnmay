# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Max


TIPOS_PERSONAS = (
        (1, 'NATURAL'),
        (2, 'JURIDICO'),
    )


MESES = (
        (1, 'ENERO'),
        (2, 'FEBRERO'),
        (3, 'MARZO'),
        (4, 'ABRIL'),
        (5, 'MAYO'),
        (6, 'JUNIO'),
        (7, 'JULIO'),
        (8, 'AGOSTO'),
        (9, 'SEPTIEMBRE'),
        (10, 'OCTUBRE'),
        (11, 'NOVIEMBRE'),
        (12, 'DICIEMBRE'),
    )


def get_mes(numero):
    return MESES[int(numero - 1)][1]


def get_code(entidad, length=4):
        model = type(entidad)
        code = ''
        sets = model.objects.filter(code__isnull=False)
        if sets:
            maxi = str(sets.aggregate(Max('code'))['code__max'])
            if maxi:
                consecutivo = list(range(1, int(maxi)))
                ocupados = list(sets.values_list('code',
                flat=True))
                n = 0
                for l in ocupados:
                    ocupados[n] = int(str(l))
                    n += 1
                disponibles = list(set(consecutivo) - set(ocupados))
                if len(disponibles) > 0:
                    code = min(disponibles)
                else:
                    code = max(ocupados) + 1
        else:
            code = 1
        return str(code).zfill(length)


class base(models.Model):

    def __iter__(self):
        for field_name in self._meta.get_all_field_names():
            try:
                value = getattr(self, field_name)
            except:
                value = None
            yield (field_name, value)

    class Meta:
        abstract = True


class base_entidad(base):
    code = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="codigo")
    name = models.CharField(max_length=100, verbose_name="nombre",
        null=True)

    class Meta:
        abstract = True


class base_documento(base):
    documento_fecha = models.DateTimeField(null=True, blank=True)
    documento_numero = models.CharField(max_length=75, null=True, blank=True)
    documento_tipo = models.CharField(max_length=75, null=True, blank=True)
    documento_afectacion = models.CharField(max_length=75, null=True,
        blank=True)
    documento_pago = models.CharField(max_length=75, null=True,
        blank=True)
    documento_usuario = models.CharField(max_length=75, null=True, blank=True)
    documento_sucursal = models.CharField(max_length=75, null=True, blank=True)
    documento_bodega = models.CharField(max_length=75, null=True, blank=True)
    documento_concepto = models.CharField(max_length=600, null=True, blank=True)

    def get_afectacion(self):
        if self.documento_afectacion == "POSITIVA":
            return 1
        if self.documento_afectacion == "NEGATIVA":
            return -1

    class Meta:
        abstract = True


class base_producto(base):
    producto_codigo = models.CharField(max_length=45, null=False, blank=False)
    producto_nombre = models.CharField(max_length=200, null=False, blank=False)
    producto_marca = models.CharField(max_length=75, null=True, blank=False)
    producto_categoria = models.CharField(max_length=75, null=True,
        blank=False)
    producto_cantidad = models.FloatField()
    producto_costo = models.FloatField()
    producto_precio = models.FloatField()
    producto_descuento = models.FloatField()

    class Meta:
        abstract = True


class base_cliente(base):
    cliente_codigo = models.CharField(max_length=45, null=False, blank=False)
    cliente_nombre = models.CharField(max_length=200, null=False, blank=False)
    cliente_identificacion = models.CharField(max_length=100, null=True,
        verbose_name="identificacion", help_text="numero ruc o cedula")
    cliente_telefono = models.CharField(max_length=100, null=True)
    cliente_direccion = models.CharField(max_length=200, null=True)
    cliente_email = models.EmailField(max_length=150, null=True)

    class Meta:
        abstract = True
