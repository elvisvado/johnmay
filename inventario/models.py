from django.db import models


class Producto(models.Model):
    bodega = models.CharField(max_length=60, null=True)
    codigo = models.CharField(max_length=30)
    descripcion = models.CharField(max_length=250)
    marca = models.CharField(max_length=60)
    categoria = models.CharField(max_length=60)
    rack = models.CharField(max_length=4)
    columna = models.CharField(max_length=2)
    fila = models.CharField(max_length=2)
    costo = models.FloatField()
    existencia = models.FloatField()
    conteo1 = models.FloatField(null=True, blank=True, default=0.0)
    conteo2 = models.FloatField(null=True, blank=True, default=0.0)
    conteo3 = models.FloatField(null=True, blank=True, default=0.0)
    con_diferencia = models.BooleanField(default=True)
    diferencia_cantidad = models.FloatField(null=True, blank=True, default=0.0)
    diferencia_importe = models.FloatField(null=True, blank=True, default=0.0)

    def __unicode__(self):
        return self.codigo + ' - ' + self.descripcion

    class Meta:
        ordering = ['rack', 'columna', 'fila', 'codigo']

    def verificar_diferencia(self):
        if self.existencia == self.conteo1:
            return False
        if self.existencia == self.conteo2:
            return False
        if self.existencia == self.conteo3:
            return False
        return True

    def get_diferencia_cantidad(self):
        if self.con_diferencia:
            minima = abs(self.existencia - self.conteo1)
            if minima > abs(self.existencia - self.conteo2):
                minima = abs(self.existencia - self.conteo2)
            if minima > abs(self.existencia - self.conteo3):
                minima = abs(self.existencia - self.conteo3)
            return minima
        else:
            return 0.0

    def get_diferencia_importe(self):
        return round(self.get_diferencia_cantidad() * self.costo, 2)

    def save(self, *args, **kwargs):
        self.con_diferencia = self.verificar_diferencia()
        self.diferencia_cantidad = self.get_diferencia_cantidad()
        self.diferencia_importe = self.get_diferencia_importe()
        super(Producto, self).save()

