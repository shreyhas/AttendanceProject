# Generated by Django 3.1.3 on 2020-12-02 15:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_auto_20201202_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otpverification',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 2, 21, 2, 27, 591459)),
        ),
        migrations.AlterField(
            model_name='parentrequest',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 21, 2, 27, 593454), null=True),
        ),
    ]