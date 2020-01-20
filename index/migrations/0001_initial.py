# Generated by Django 3.0 on 2019-12-11 06:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('wd_id', models.CharField(max_length=10)),
                ('c_lat', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Широта')),
                ('c_lon', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Долгота')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('wd_id', models.CharField(max_length=10)),
                ('capital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.City', verbose_name='Центр')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('text', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('wd_id', models.CharField(max_length=10)),
                ('c_lat', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Широта')),
                ('c_lon', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Долгота')),
                ('status', models.CharField(blank=True, choices=[('s', 'Опубликовано'), ('e', 'В черновике')], default='e', max_length=1, verbose_name='Статус')),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.Cat', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Место',
                'verbose_name_plural': 'Места',
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Название')),
                ('wd_id', models.CharField(max_length=10)),
                ('capital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.City', verbose_name='Центр')),
            ],
            options={
                'verbose_name': 'Район',
                'verbose_name_plural': 'Районы',
            },
        ),
    ]