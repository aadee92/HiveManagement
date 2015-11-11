# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0010_auto_20151105_0725'),
    ]

    operations = [
        migrations.AddField(
            model_name='field',
            name='weather_conditions',
            field=models.CharField(max_length=100, blank=True),
        ),
    ]
