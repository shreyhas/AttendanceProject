# Generated by Django 3.1.3 on 2020-12-03 10:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0025_auto_20201202_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 3, 16, 27, 21, 916680)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 3, 16, 27, 21, 915683), null=True),
        ),
    ]
