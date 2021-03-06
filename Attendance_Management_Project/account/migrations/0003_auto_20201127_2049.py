# Generated by Django 3.1.3 on 2020-11-27 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='grades',
            field=models.CharField(help_text='Separate grades by commas.', max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='teacher',
            name='is_coordinator',
            field=models.BooleanField(default=False, help_text='Select only if Teacher is Coordinator.'),
        ),
    ]
