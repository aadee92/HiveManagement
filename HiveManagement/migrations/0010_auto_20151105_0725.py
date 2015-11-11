# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0009_auto_20151105_0719'),
    ]

    operations = [
        migrations.CreateModel(
            name='PalletReport',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('number_alive', models.SmallIntegerField(default=4)),
                ('field', models.ForeignKey(to='HiveManagement.Field')),
                ('tag', models.ForeignKey(to='HiveManagement.Tag')),
            ],
        ),
        migrations.RemoveField(
            model_name='palletcheckin',
            name='field',
        ),
        migrations.RemoveField(
            model_name='palletcheckin',
            name='tag',
        ),
        migrations.DeleteModel(
            name='PalletCheckIn',
        ),
    ]
