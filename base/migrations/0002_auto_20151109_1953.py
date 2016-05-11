# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='identificacion',
            field=models.CharField(help_text=b'numero ruc o cedula', max_length=100, null=True, verbose_name=b'identificacion'),
            preserve_default=True,
        ),
    ]
