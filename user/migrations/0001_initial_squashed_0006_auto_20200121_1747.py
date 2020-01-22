# Generated by Django 3.0.2 on 2020-01-23 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import imagefield.fields


class Migration(migrations.Migration):

    replaces = [('user', '0001_initial'), ('user', '0002_auto_20200115_1154'), ('user', '0003_auto_20200115_1255'), ('user', '0004_auto_20200115_1328'), ('user', '0005_auto_20200120_1555'), ('user', '0006_auto_20200121_1747')]

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('index', '0020_remove_city_type_place'),
        ('index', '0021_auto_20200115_1154'),
        ('index', '0028_auto_20200120_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500, verbose_name='Краткая информация')),
                ('instagram', models.CharField(blank=True, max_length=50)),
                ('city', models.ForeignKey(help_text='Используется для показа пути от этого места до начала маршрута.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.City', verbose_name='Населённый пункт')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('done_place', models.ManyToManyField(db_table='done_user_place', related_name='done_place', to='index.Place', verbose_name='Пройденные места')),
                ('want_place', models.ManyToManyField(db_table='want_user_place', related_name='want_place', to='index.Place', verbose_name='Планируемые места')),
                ('like_place', models.ManyToManyField(db_table='like_user_place', related_name='like_place', to='index.Place', verbose_name='Избранное')),
                ('image', imagefield.fields.ImageField(blank=True, height_field='image_height', upload_to='', verbose_name='Изображение', width_field='image_width')),
                ('image_height', models.PositiveIntegerField(blank=True, editable=False, null=True)),
                ('image_ppoi', imagefield.fields.PPOIField(default='0.5x0.5', max_length=20)),
                ('image_width', models.PositiveIntegerField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
    ]