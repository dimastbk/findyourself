# Generated by Django 3.0 on 2019-12-12 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0006_district_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='image',
            field=models.ImageField(blank=True, default='', upload_to='', verbose_name='Изображение'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='wd_id',
            field=models.CharField(blank=True, default='', max_length=10),
            preserve_default=False,
        ),
    ]
