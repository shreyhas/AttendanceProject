# Generated by Django 3.1.3 on 2020-12-01 16:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_auto_20201201_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='parentrequest',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 1, 21, 49, 6, 746608), null=True),
        ),
        migrations.AlterField(
            model_name='otpverification',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 1, 21, 49, 6, 743613)),
        ),
    ]
