# Generated by Django 3.1.3 on 2020-11-28 04:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0017_auto_20201127_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 11, 28, 10, 25, 41, 604523)),
        ),
    ]