# Generated by Django 3.1.3 on 2020-12-03 10:58

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0026_auto_20201203_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 3, 16, 28, 45, 698863)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 3, 16, 28, 45, 697865), null=True),
        ),
    ]
