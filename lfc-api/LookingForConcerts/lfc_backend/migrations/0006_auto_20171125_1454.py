# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-25 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lfc_backend', '0005_concertimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='user/')),
            ],
        ),
        migrations.RemoveField(
            model_name='registereduser',
            name='avatar',
        ),
        migrations.AddField(
            model_name='concert',
            name='image',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AddField(
            model_name='concert',
            name='seller_url',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='registereduser',
            name='image',
            field=models.CharField(blank=True, max_length=300),
        ),
        migrations.AlterField(
            model_name='concertimage',
            name='image',
            field=models.FileField(upload_to='concert/'),
        ),
    ]