# Generated by Django 2.1.7 on 2019-04-18 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0002_variable_name_cs'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='name_cs',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]