# Generated by Django 3.0.4 on 2020-03-23 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_auto_20200323_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(verbose_name='time'),
        ),
    ]
