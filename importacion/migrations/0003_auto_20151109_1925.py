# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importacion', '0002_auto_20151109_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='cliente_email',
            field=models.EmailField(max_length=150, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documento',
            name='cliente_identificacion',
            field=models.CharField(help_text=b'numero ruc o cedula', max_length=100, null=True, verbose_name=b'identificacion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documento',
            name='cliente_telefono',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
