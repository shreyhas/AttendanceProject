# Generated by Django 3.1.3 on 2020-11-17 16:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0007_remove_attendancestudent_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 11, 17, 21, 51, 13, 558638)),
        ),
    ]