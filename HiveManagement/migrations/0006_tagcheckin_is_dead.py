# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0005_auto_20151104_0619'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagcheckin',
            name='is_dead',
            field=models.BooleanField(default=False),
        ),
    ]
