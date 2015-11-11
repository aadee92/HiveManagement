# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0008_auto_20151104_2229'),
    ]

    operations = [
        migrations.CreateModel(
            name='PalletCheckIn',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('number_alive', models.SmallIntegerField(default=4)),
                ('field', models.ForeignKey(to='HiveManagement.Field')),
                ('tag', models.ForeignKey(to='HiveManagement.Tag')),
            ],
        ),
        migrations.RemoveField(
            model_name='tagcheckin',
            name='field',
        ),
        migrations.RemoveField(
            model_name='tagcheckin',
            name='tag',
        ),
        migrations.DeleteModel(
            name='TagCheckIn',
        ),
    ]
