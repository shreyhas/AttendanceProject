# Generated by Django 3.1.3 on 2020-12-05 15:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0029_auto_20201204_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 5, 20, 45, 14, 545695)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 5, 20, 45, 14, 543803), null=True),
        ),
    ]
