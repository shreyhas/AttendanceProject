# Generated by Django 3.1.3 on 2020-11-27 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0014_auto_20201127_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 11, 27, 20, 45, 45, 467555)),
        ),
    ]