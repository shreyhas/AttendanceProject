# Generated by Django 3.1.3 on 2020-12-02 15:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_auto_20201202_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverification',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 21, 22, 28, 473169)),
        ),
        migrations.AlterField(
            model_name='parentrequest',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 21, 22, 28, 474203), null=True),
        ),
    ]