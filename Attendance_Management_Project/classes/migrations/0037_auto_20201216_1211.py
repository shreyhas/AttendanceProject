# Generated by Django 3.1.3 on 2020-12-16 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0036_auto_20201216_1210'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classmodel',
            name='is_homeroom',
        ),
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 11, 26, 424914)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 11, 26, 423875), null=True),
        ),
    ]
