# Generated by Django 3.1.3 on 2020-12-02 15:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0022_auto_20201201_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 20, 48, 18, 871940), null=True),
        ),
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 2, 20, 48, 18, 872937)),
        ),
    ]
