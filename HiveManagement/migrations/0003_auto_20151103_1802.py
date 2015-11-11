# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0002_auto_20151103_0209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='field',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='field',
            name='owner',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
