# Generated by Django 3.1.3 on 2020-12-16 06:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_auto_20201216_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverification',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 16, 12, 11, 26, 433841)),
        ),
        migrations.AlterField(
            model_name='parentrequest',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 11, 26, 438374), null=True),
        ),
    ]
