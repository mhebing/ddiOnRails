# Generated by Django 2.1.5 on 2019-01-17 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0008_auto_20190117_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='script',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
