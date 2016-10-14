# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_auto_20160411_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='existencia',
            name='bodega_codigo',
            field=models.CharField(max_length=65, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='existencia',
            name='producto_codigo',
            field=models.CharField(max_length=65, null=True),
            preserve_default=True,
        ),
    ]
