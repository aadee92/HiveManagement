# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=25)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('description', models.CharField(max_length=250)),
                ('owner', models.CharField(max_length=16)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('uniqueTID', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TagCheckIn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('field', models.ForeignKey(to='HiveManagement.Field')),
                ('tag', models.ForeignKey(to='HiveManagement.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=16)),
                ('description', models.CharField(max_length=250)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='WorkLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date_work', models.DateField(auto_now_add=True)),
                ('hives_alive', models.IntegerField()),
                ('field', models.ForeignKey(to='HiveManagement.Field')),
                ('task', models.ForeignKey(to='HiveManagement.Task')),
                ('team', models.ForeignKey(to='HiveManagement.Team')),
            ],
        ),
    ]
