# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HiveManagement', '0007_auto_20151104_2154'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(default='Unknown', max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='field',
            name='source_region',
            field=models.ForeignKey(to='HiveManagement.Region', blank=True, null=True),
        ),
    ]
