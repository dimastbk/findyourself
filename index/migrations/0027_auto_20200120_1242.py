# Generated by Django 3.0.2 on 2020-01-20 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0026_auto_20200120_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='ig_id',
            field=models.CharField(blank=True, max_length=20, verbose_name='Локация в IG'),
        ),
    ]