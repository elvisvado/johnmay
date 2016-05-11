# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0004_auto_20151223_1440'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estadistica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.PositiveIntegerField(null=True)),
                ('month', models.PositiveIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='tasa_cambio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('oficial', models.FloatField(default=0.0)),
                ('venta', models.FloatField(default=0.0)),
                ('compra', models.FloatField(default=0.0)),
                ('fecha', models.DateField()),
                ('registro', models.DateTimeField()),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'verbose_name': 'Registro',
                'verbose_name_plural': 'mesa de cambio del sistema',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tipodoc',
            name='afecta_costo',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tipodoc',
            name='kardex_global',
            field=models.NullBooleanField(verbose_name=b'aparece en kardex global'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documento',
            name='cliente',
            field=models.ForeignKey(blank=True, to='base.Cliente', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documento',
            name='tipopago',
            field=models.ForeignKey(blank=True, to='base.TipoPago', null=True),
            preserve_default=True,
        ),
    ]
