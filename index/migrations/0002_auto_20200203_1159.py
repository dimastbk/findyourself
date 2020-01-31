# Generated by Django 3.0.2 on 2020-02-03 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0001_initial_squashed_0029_auto_20200121_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='create_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='type',
            name='icon',
            field=models.CharField(max_length=200, verbose_name='Название иконки'),
        ),
        migrations.AlterField(
            model_name='type',
            name='title_pl',
            field=models.CharField(max_length=200, verbose_name='Множественное название'),
        ),
    ]
