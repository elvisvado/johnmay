# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documento_fecha', models.DateTimeField(null=True, blank=True)),
                ('documento_numero', models.CharField(max_length=10, null=True, blank=True)),
                ('documento_tipo', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_afectacion', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_usuario', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_sucursal', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_bodega', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_concepto', models.CharField(max_length=600, null=True, blank=True)),
                ('producto_codigo', models.CharField(max_length=45)),
                ('producto_nombre', models.CharField(max_length=200)),
                ('producto_marca', models.CharField(max_length=75, null=True)),
                ('producto_categoria', models.CharField(max_length=75, null=True)),
                ('producto_cantidad', models.FloatField()),
                ('producto_costo', models.FloatField()),
                ('producto_precio', models.FloatField()),
                ('producto_descuento', models.FloatField()),
                ('cliente_codigo', models.CharField(max_length=45)),
                ('cliente_nombre', models.CharField(max_length=200)),
                ('cliente_identificacion', models.CharField(help_text=b'numero ruc o cedula', max_length=30, null=True, verbose_name=b'identificacion')),
                ('cliente_telefono', models.CharField(max_length=30, null=True)),
                ('cliente_direccion', models.CharField(max_length=200, null=True)),
                ('cliente_email', models.EmailField(max_length=60, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documento_fecha', models.DateTimeField(null=True, blank=True)),
                ('documento_numero', models.CharField(max_length=10, null=True, blank=True)),
                ('documento_tipo', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_afectacion', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_usuario', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_sucursal', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_bodega', models.CharField(max_length=75, null=True, blank=True)),
                ('documento_concepto', models.CharField(max_length=600, null=True, blank=True)),
                ('producto_codigo', models.CharField(max_length=45)),
                ('producto_nombre', models.CharField(max_length=200)),
                ('producto_marca', models.CharField(max_length=75, null=True)),
                ('producto_categoria', models.CharField(max_length=75, null=True)),
                ('producto_cantidad', models.FloatField()),
                ('producto_costo', models.FloatField()),
                ('producto_precio', models.FloatField()),
                ('producto_descuento', models.FloatField()),
                ('ubicacion', models.CharField(max_length=20, null=True, blank=True)),
            ],
            options={
                'verbose_name': 'producto',
                'verbose_name_plural': 'inventario inicial',
            },
            bases=(models.Model,),
        ),
    ]
