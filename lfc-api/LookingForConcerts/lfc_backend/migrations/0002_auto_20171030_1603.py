# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-30 16:03
from __future__ import unicode_literals

from django.db import migrations
import lfc_backend.managers


class Migration(migrations.Migration):

    dependencies = [
        ('lfc_backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='registereduser',
            managers=[
                ('objects', lfc_backend.managers.UserManager()),
            ],
        ),
    ]