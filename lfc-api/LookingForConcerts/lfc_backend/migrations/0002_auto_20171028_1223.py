# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 09:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lfc_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concert',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='concerts', to='lfc_backend.Location'),
        ),
    ]
