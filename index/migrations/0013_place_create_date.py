# Generated by Django 3.0 on 2019-12-16 03:55

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0012_type_title_pl'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='create_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
