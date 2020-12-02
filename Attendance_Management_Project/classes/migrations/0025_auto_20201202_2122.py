# Generated by Django 3.1.3 on 2020-12-02 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0024_auto_20201202_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 21, 22, 28, 467186)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 21, 22, 28, 466189), null=True),
        ),
    ]