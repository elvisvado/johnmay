# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bodega', models.CharField(max_length=60, null=True)),
                ('codigo', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=250)),
                ('marca', models.CharField(max_length=60)),
                ('categoria', models.CharField(max_length=60)),
                ('rack', models.CharField(max_length=4)),
                ('columna', models.CharField(max_length=2)),
                ('fila', models.CharField(max_length=2)),
                ('costo', models.FloatField()),
                ('existencia', models.FloatField()),
                ('conteo1', models.FloatField(default=0.0, null=True, blank=True)),
                ('conteo2', models.FloatField(default=0.0, null=True, blank=True)),
                ('conteo3', models.FloatField(default=0.0, null=True, blank=True)),
                ('con_diferencia', models.BooleanField(default=True)),
                ('diferencia_cantidad', models.FloatField(default=0.0, null=True, blank=True)),
                ('diferencia_importe', models.FloatField(default=0.0, null=True, blank=True)),
            ],
            options={
                'ordering': ['rack', 'columna', 'fila', 'codigo'],
            },
            bases=(models.Model,),
        ),
    ]
