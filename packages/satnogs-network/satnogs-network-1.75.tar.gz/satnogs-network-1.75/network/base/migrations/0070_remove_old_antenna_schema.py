# Generated by Django 1.11.29 on 2020-04-26 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0069_increase_range_frequency_limits'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='station',
            name='antenna',
        ),
        migrations.DeleteModel(
            name='Antenna',
        ),
    ]
