from django.db import models
from django.contrib.auth.models import User
from .base import *
from django.db.models import Sum


def totalizar(a, b):
    try:
        return round(a * b, 2)
    except:
        return 0.0


class Entidad(base_entidad):
    activo = models.BooleanField(default=True)

    def __unicode__(self):
        if self.code and self.name:
            return self.name + " - " + str(self.code)
        elif self.name:
            return self.name
        elif self.code:
            return str(self.code)
        else:
            return ''

    @staticmethod
    def autocomplete_search_fields():
        return ("code__iexact", "name__icontains",)

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = get_code(self)
        super(Entidad, self).save()

    class Meta:
        abstract = True
        ordering = ['name']


class Sucursal(Entidad):
    pbx = models.CharField(max_length=25, null=True, blank=True)
    direccion = models.TextField(max_length=250, null=True, blank=True)
    ruc = models.CharField(max_length=25, null=True, blank=True)
    slogan = models.CharField(max_length=100, null=True, blank=True)
    logo = models.ImageField(upload_to='media/logos', null=True, blank=True)
    web = models.URLField(max_length=25, null=True, blank=True)
    email = models.EmailField(max_length=25, null=True, blank=True)

    class Meta:
        verbose_name_plural = "sucursales"


class Bodega(Entidad):
    sucursal = models.ForeignKey(Sucursal, null=True)


User.add_to_class('sucursal', models.ForeignKey(Sucursal, null=True))


class Marca(Entidad):
    pass


class Categoria(Entidad):
    pass


class Producto(Entidad):
    no_parte = models.CharField(max_length=25, null=True, blank=True,
    verbose_name="numero de parte")
    medida = models.CharField(max_length=25, null=True, blank=True)
    modelo = models.CharField(max_length=60, null=True, blank=True)
    nauca = models.CharField(max_length=25, null=True, blank=True,
        verbose_name="codigo nauca")

    caducidad = models.DateField(null=True, blank=True,
        verbose_name="fecha de caducidad")

    costo = models.FloatField(default=0.0)
    precio = models.FloatField(default=0.0)
    tc = models.FloatField(default=0.0)

    excento = models.BooleanField(default=False)
    almacena = models.BooleanField(default=True)
    vende = models.BooleanField(default=False)
    compra = models.BooleanField(default=False)

    minimo = models.FloatField(null=True, blank=True,
        verbose_name="existencia minima requerida")
    maximo = models.FloatField(null=True, blank=True,
        verbose_name="existencia maxima permitida")

    TIPOS_CLACIFICACION = (('A', 'EXCELENTE'), ('B', 'BUENO'),
        ('C', 'REGULAR'), ('D', 'MALO'))
    clasificacion = models.CharField(max_length=1, choices=TIPOS_CLACIFICACION,
        help_text="clasificacion o comportamiento de ventas", null=True)

    marca = models.ForeignKey(Marca, null=True, blank=True)
    categoria = models.ForeignKey(Categoria, null=True, blank=True)

    def existencias(self):
        return Existencia.objects.filter(producto=self)

    def existencia_total(self):
        if self.existencias():
            return self.existencias().aggregate(
                Sum('existencia'))['existencia__sum']
        else:
            return 0


class Existencia(models.Model):
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    existencia_disponible = models.FloatField(default=0.0)
    existencia_real = models.FloatField(default=0.0)
    ubicacion = models.CharField(max_length=15, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Existencias en bodega"


class Serie(models.Model):
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)
    numero = models.CharField(max_length=50, null=False, blank=False)


class TipoPago(Entidad):
    capitalizable = models.BooleanField(default=False)


class Cliente(Entidad):
    identificacion = models.CharField(max_length=100, null=True,
        verbose_name="identificacion", help_text="numero ruc o cedula")
    telefono = models.CharField(max_length=30, null=True, blank=True)
    direccion = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=60, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)
    tipo_persona = models.IntegerField(choices=TIPOS_PERSONAS,
        null=True, blank=True, verbose_name="tipo de cliente")
    limite_credito = models.FloatField(null=True, blank=True)
    limite_descuento = models.FloatField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.code is None or self.code == '':
            self.code = get_code(self, 6)
        super(Entidad, self).save()


class Vendedor(models.Model):
    username = models.CharField(max_length=75)
    sucursal = models.ForeignKey(Sucursal, null=True,
        related_name="facturacion_vendedor_sucursal")

    class Meta:
        managed = False
        db_table = "auth_user"
        verbose_name_plural = "vendedores"


TIPOS_AFECTACION = (
                (1, "POSITIVA"),
                (0, "SIN AFECTACION"),
                (-1, "NEGATIVA"),
                    )


class TipoDoc(Entidad):
    afectacion = models.IntegerField(choices=TIPOS_AFECTACION)
    afecta_costo = models.NullBooleanField()


class Documento(models.Model):

    user = models.ForeignKey(User)
    numero = models.PositiveIntegerField(null=True, blank=True)
    tipopago = models.ForeignKey(TipoPago, null=True)
    tipodoc = models.ForeignKey(TipoDoc, null=True)
    sucursal = models.ForeignKey(Sucursal)
    fecha = models.DateTimeField()
    fecha_vence = models.DateField(null=True, blank=True)
    comentarios = models.TextField(max_length=150, null=True, blank=True)

    subtotal = models.FloatField(default=0.0)
    descuento = models.FloatField(default=0.0)
    iva = models.FloatField(default=0.0)
    ir = models.FloatField(default=0.0)
    al = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
    costo = models.FloatField(default=0.0)
    saldo = models.FloatField(default=0.0)

    utilidad = models.FloatField(default=0.0)
    factor = models.FloatField(default=0.0)

    impreso = models.BooleanField(default=False)
    aplicado = models.BooleanField(default=False)
    contabilizado = models.BooleanField(default=False)

    cliente = models.ForeignKey(Cliente, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.tipodoc.name, self.numero)

    def detalle(self):
        return Detalle.objects.filter(documento=self)

    def aplicar(self):
        if self.detalle():
            for d in self.detalle():
                d.aplicar()
        self.calcular()
        self.aplicado = True
        self.save()
        return self

    def calcular(self):
        if self.detalle():
            for d in self.detalle():
                d.calcular()
            self.subtotal = round(self.detalle().aggregate(Sum(
                'precio_total'))['precio_total__sum'], 2)
            self.descuento = round(self.detalle().aggregate(Sum(
                'descuento_total'))['descuento_total__sum'], 2)
            self.costo = round(self.detalle().aggregate(Sum(
                'costo_total'))['costo_total__sum'], 2)
            self.iva = round((self.subtotal - self.descuento) * 0.15, 2)
            self.total = round((self.subtotal - self.descuento + self.iva - (
                self.ir + self.al)), 2)
            self.utilidad = round((self.subtotal - self.descuento) - self.costo,
                2)
            if self.costo > 0:
                self.factor = round((
                    self.subtotal - self.descuento) / self.costo,
                    1)
            self.save()


class Detalle(models.Model):
    documento = models.ForeignKey(Documento)
    producto = models.ForeignKey(Producto)
    bodega = models.ForeignKey(Bodega)

    modelo = models.CharField(max_length=60, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)

    producto_cantidad = models.FloatField(default=0.0)
    producto_precio_unitario = models.FloatField(default=0.0)
    producto_costo_unitario = models.FloatField(default=0.0)
    producto_descuento_unitario = models.FloatField(default=0.0)
    producto_existencia = models.FloatField(default=0.0)
    producto_saldo = models.FloatField(default=0.0)
    producto_costo_promedio = models.FloatField(default=0.0)

    precio_total = models.FloatField(default=0.0)
    descuento_total = models.FloatField(default=0.0)
    costo_total = models.FloatField(default=0.0)

    utilidad = models.FloatField(default=0.0)
    factor = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "detalle de documentos"

    def __unicode__(self):
        return '%s %s - %s - %s' % (self.documento.tipodoc.name,
            self.documento.numero, self.producto.code,
            self.producto.name)

    def get_costo_promedio(self):
        value = 0
        if self.documento.tipodoc.afecta_costo:
            value = ((self.producto.existencia_total() * self.producto.costo)
            + (self.producto_cantidad * self.producto_costo_unitario)) / (
                self.cantidad + self.producto.existencia_total())
        else:
            value = self.producto.costo
        return value

    def aplicar(self):
        self.calcular()
        e, created = Existencia.objects.get_or_create(producto=self.producto,
            bodega=self.bodega)
        self.producto_existencia = e.existencia_disponible
        e.existencia_disponible = e.existencia_disponible + \
        (self.producto_cantidad * self.documento.tipodoc.afectacion)
        self.producto_saldo = e.existencia_disponible
        e.save()
        self.producto_costo_promedio = self.get_costo_promedio()
        self.save()
        print '%s - %s - %s - %s' % (str(self.documento.fecha),
            str(self.producto_cantidad), self.producto.name,
            self.bodega.name)
        return self

    def calcular(self):
        self.precio_total = totalizar(self.producto_cantidad,
            self.producto_precio_unitario)
        self.descuento_total = totalizar(self.producto_cantidad,
            self.producto_descuento_unitario)
        self.costo_total = totalizar(self.producto_cantidad,
            self.producto_costo_unitario)
        self.save()


class tasa_cambio(models.Model):
    oficial = models.FloatField(default=0.0)
    venta = models.FloatField(default=0.0)
    compra = models.FloatField(default=0.0)

    fecha = models.DateField()
    registro = models.DateTimeField()

    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name_plural = "mesa de cambio del sistema"
        verbose_name = "Registro"