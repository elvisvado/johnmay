# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=75)),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
                'verbose_name_plural': 'vendedores',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('identificacion', models.CharField(help_text=b'numero ruc o cedula', max_length=30, null=True, verbose_name=b'identificacion')),
                ('telefono', models.CharField(max_length=30, null=True)),
                ('direccion', models.CharField(max_length=200, null=True)),
                ('email', models.EmailField(max_length=60, null=True)),
                ('tipo_persona', models.IntegerField(blank=True, null=True, verbose_name=b'tipo de cliente', choices=[(1, b'NATURAL'), (2, b'JURIDICO')])),
                ('limite_credito', models.FloatField(null=True, blank=True)),
                ('limite_descuento', models.FloatField(null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('modelo', models.CharField(max_length=60, null=True, blank=True)),
                ('serie', models.CharField(max_length=50, null=True, blank=True)),
                ('producto_cantidad', models.FloatField(default=0.0)),
                ('producto_precio_unitario', models.FloatField(default=0.0)),
                ('producto_costo_unitario', models.FloatField(default=0.0)),
                ('producto_descuento_unitario', models.FloatField(default=0.0)),
                ('producto_existencia', models.FloatField(default=0.0)),
                ('producto_saldo', models.FloatField(default=0.0)),
                ('producto_costo_promedio', models.FloatField(default=0.0)),
                ('precio_total', models.FloatField(default=0.0)),
                ('descuento_total', models.FloatField(default=0.0)),
                ('costo_total', models.FloatField(default=0.0)),
                ('utilidad', models.FloatField(default=0.0)),
                ('factor', models.FloatField(default=0.0)),
                ('bodega', models.ForeignKey(to='base.Bodega')),
            ],
            options={
                'verbose_name_plural': 'detalle de documentos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.PositiveIntegerField(null=True, blank=True)),
                ('fecha', models.DateTimeField()),
                ('fecha_vence', models.DateField(null=True, blank=True)),
                ('comentarios', models.TextField(max_length=150, null=True, blank=True)),
                ('subtotal', models.FloatField(default=0.0)),
                ('descuento', models.FloatField(default=0.0)),
                ('iva', models.FloatField(default=0.0)),
                ('ir', models.FloatField(default=0.0)),
                ('al', models.FloatField(default=0.0)),
                ('total', models.FloatField(default=0.0)),
                ('costo', models.FloatField(default=0.0)),
                ('saldo', models.FloatField(default=0.0)),
                ('utilidad', models.FloatField(default=0.0)),
                ('factor', models.FloatField(default=0.0)),
                ('impreso', models.BooleanField(default=False)),
                ('aplicado', models.BooleanField(default=False)),
                ('contabilizado', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(to='base.Cliente', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Existencia',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('existencia_disponible', models.FloatField(default=0.0)),
                ('existencia_real', models.FloatField(default=0.0)),
                ('ubicacion', models.CharField(max_length=15, null=True, blank=True)),
                ('bodega', models.ForeignKey(to='base.Bodega')),
            ],
            options={
                'verbose_name_plural': 'Existencias en bodega',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('no_parte', models.CharField(max_length=25, null=True, verbose_name=b'numero de parte', blank=True)),
                ('medida', models.CharField(max_length=25, null=True, blank=True)),
                ('modelo', models.CharField(max_length=60, null=True, blank=True)),
                ('nauca', models.CharField(max_length=25, null=True, verbose_name=b'codigo nauca', blank=True)),
                ('caducidad', models.DateField(null=True, verbose_name=b'fecha de caducidad', blank=True)),
                ('costo', models.FloatField(default=0.0)),
                ('precio', models.FloatField(default=0.0)),
                ('tc', models.FloatField(default=0.0)),
                ('excento', models.BooleanField(default=False)),
                ('almacena', models.BooleanField(default=True)),
                ('vende', models.BooleanField(default=False)),
                ('compra', models.BooleanField(default=False)),
                ('minimo', models.FloatField(null=True, verbose_name=b'existencia minima requerida', blank=True)),
                ('maximo', models.FloatField(null=True, verbose_name=b'existencia maxima permitida', blank=True)),
                ('clasificacion', models.CharField(help_text=b'clasificacion o comportamiento de ventas', max_length=1, null=True, choices=[(b'A', b'EXCELENTE'), (b'B', b'BUENO'), (b'C', b'REGULAR'), (b'D', b'MALO')])),
                ('categoria', models.ForeignKey(blank=True, to='base.Categoria', null=True)),
                ('marca', models.ForeignKey(blank=True, to='base.Marca', null=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Serie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('numero', models.CharField(max_length=50)),
                ('bodega', models.ForeignKey(to='base.Bodega')),
                ('producto', models.ForeignKey(to='base.Producto')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('pbx', models.CharField(max_length=25, null=True, blank=True)),
                ('direccion', models.TextField(max_length=250, null=True, blank=True)),
                ('ruc', models.CharField(max_length=25, null=True, blank=True)),
                ('slogan', models.CharField(max_length=100, null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'media/logos', blank=True)),
                ('web', models.URLField(max_length=25, null=True, blank=True)),
                ('email', models.EmailField(max_length=25, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'sucursales',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoDoc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('afectacion', models.IntegerField(choices=[(1, b'POSITIVA'), (0, b'SIN AFECTACION'), (-1, b'NEGATIVA')])),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=25, null=True, verbose_name=b'codigo', blank=True)),
                ('name', models.CharField(max_length=100, null=True, verbose_name=b'nombre')),
                ('activo', models.BooleanField(default=True)),
                ('capitalizable', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='existencia',
            name='producto',
            field=models.ForeignKey(to='base.Producto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documento',
            name='sucursal',
            field=models.ForeignKey(to='base.Sucursal'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documento',
            name='tipodoc',
            field=models.ForeignKey(to='base.TipoDoc', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documento',
            name='tipopago',
            field=models.ForeignKey(to='base.TipoPago', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documento',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalle',
            name='documento',
            field=models.ForeignKey(to='base.Documento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='detalle',
            name='producto',
            field=models.ForeignKey(to='base.Producto'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bodega',
            name='sucursal',
            field=models.ForeignKey(to='base.Sucursal'),
            preserve_default=True,
        ),
    ]
