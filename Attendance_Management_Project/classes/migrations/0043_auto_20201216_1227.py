# Generated by Django 3.1.3 on 2020-12-16 06:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0042_auto_20201216_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendancestudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 27, 17, 859271)),
        ),
        migrations.AlterField(
            model_name='classmodel',
            name='block',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='classmodel',
            name='subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='classes.subject'),
        ),
        migrations.AlterField(
            model_name='classstudent',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 12, 16, 12, 27, 17, 858128), null=True),
        ),
    ]
