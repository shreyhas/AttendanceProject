# Generated by Django 3.1.3 on 2020-12-16 06:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_auto_20201216_1153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='classteachergrades',
        ),
        migrations.RemoveField(
            model_name='teacher',
            name='is_classteacher',
        ),
    ]
