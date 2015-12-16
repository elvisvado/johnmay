# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('importacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='documento',
            name='documento_pago',
            field=models.CharField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inventario',
            name='documento_pago',
            field=models.CharField(max_length=75, null=True, blank=True),
            preserve_default=True,
        ),
    ]
