# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importacion', '0003_auto_20151109_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='documento_numero',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='inventario',
            name='documento_numero',
            field=models.IntegerField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
