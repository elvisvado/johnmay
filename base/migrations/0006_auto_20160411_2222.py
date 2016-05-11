# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20160317_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documento',
            name='numero',
            field=models.CharField(max_length=65, null=True, blank=True),
            preserve_default=True,
        ),
    ]
