# Generated by Django 1.11.7 on 2017-12-24 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0031_migrate_vetted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='observation',
            name='vetted_status',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('good', 'Good'), ('bad', 'Bad'), ('failed', 'Failed')], default='unknown', max_length=20),
        ),
    ]
