# Generated by Django 3.0 on 2019-12-13 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0010_auto_20191213_1055'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='tag',
            new_name='district',
        ),
        migrations.AddField(
            model_name='city',
            name='ae1',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.District', verbose_name='Район'),
        ),
        migrations.AddField(
            model_name='city',
            name='ae2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.Region', verbose_name='Регион'),
        ),
        migrations.AddField(
            model_name='place',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.City', verbose_name='Населённый пункт'),
        ),
        migrations.AddField(
            model_name='place',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.Region', verbose_name='Регион'),
        ),
    ]
