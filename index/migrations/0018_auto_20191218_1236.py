# Generated by Django 3.0 on 2019-12-18 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0017_auto_20191218_1234'),
    ]

    operations = [
        migrations.RenameField(
            model_name='route',
            old_name='title',
            new_name='rt_title',
        ),
    ]