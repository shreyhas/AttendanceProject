# Generated by Django 3.1.3 on 2020-12-16 06:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0038_auto_20201216_1218'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HomeroomClassModel',
        ),
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 21, 3, 979480)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 21, 3, 977484), null=True),
        ),
    ]
