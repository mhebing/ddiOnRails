# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-09-26 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20180926_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dataset',
            name='label_de',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='variable',
            name='label_de',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
