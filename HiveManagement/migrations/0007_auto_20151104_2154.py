# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0006_tagcheckin_is_dead'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tagcheckin',
            name='is_dead',
        ),
        migrations.AddField(
            model_name='tagcheckin',
            name='number_alive',
            field=models.SmallIntegerField(default=4),
        ),
    ]
