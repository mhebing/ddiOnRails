# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-26 14:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_auto_20171017_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='label_de',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='variable',
            name='label_de',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
