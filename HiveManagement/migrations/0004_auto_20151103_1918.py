# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0003_auto_20151103_1802'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='county',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='locality',
            field=models.CharField(max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='field',
            name='state',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
