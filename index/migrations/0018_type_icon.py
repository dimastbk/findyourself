# Generated by Django 3.0 on 2019-12-19 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0017_auto_20191218_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='icon',
            field=models.CharField(default='', max_length=200, verbose_name='Название иконки'),
            preserve_default=False,
        ),
    ]
