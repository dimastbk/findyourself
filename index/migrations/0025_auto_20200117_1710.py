# Generated by Django 3.0.2 on 2020-01-17 07:10

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0024_remove_route_ls'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='ls',
            field=django.contrib.gis.db.models.fields.LineStringField(blank=True, dim=3, null=True, srid=4326, verbose_name='Маршрут'),
        ),
        migrations.AddField(
            model_name='route',
            name='ls2',
            field=django.contrib.gis.db.models.fields.LineStringField(blank=True, null=True, srid=4326, verbose_name='2D-маршрут'),
        ),
    ]
