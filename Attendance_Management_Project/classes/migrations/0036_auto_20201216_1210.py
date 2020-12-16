# Generated by Django 3.1.3 on 2020-12-16 06:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0035_auto_20201216_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='classmodel',
            name='is_homeroom',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 10, 44, 692593)),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 10, 44, 691597), null=True),
        ),
    ]
