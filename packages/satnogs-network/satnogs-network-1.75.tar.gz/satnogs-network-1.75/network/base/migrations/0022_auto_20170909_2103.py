# Generated by Django 1.11.4 on 2017-09-09 21:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    def disable_db_checks(apps, schema_editor):
        from django.db import connections, DEFAULT_DB_ALIAS
        connection = connections[DEFAULT_DB_ALIAS]
        if 'mysql' in connection.settings_dict['ENGINE']:
            cursor = connection.cursor()
            cursor.execute('SET foreign_key_checks = 0')

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0021_auto_20170813_1258'),
    ]

    operations = [
        migrations.RunPython(disable_db_checks),

        migrations.AddField(
            model_name='demoddata',
            name='observation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='demoddata', to='base.Observation'),
        ),
        migrations.AddField(
            model_name='observation',
            name='ground_station',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='base.Station'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='observation',
            name='max_altitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observation',
            name='payload',
            field=models.FileField(blank=True, null=True, upload_to='data_payloads'),
        ),
        migrations.AddField(
            model_name='observation',
            name='rise_azimuth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observation',
            name='set_azimuth',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observation',
            name='vetted_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='observation',
            name='vetted_status',
            field=models.CharField(choices=[('unknown', 'Unknown'), ('verified', 'Verified'), ('data_not_verified', 'Has Data, Not Verified'), ('no_data', 'No Data')], default='unknown', max_length=20),
        ),
        migrations.AddField(
            model_name='observation',
            name='vetted_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='observations_vetted', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='observation',
            name='waterfall',
            field=models.ImageField(blank=True, null=True, upload_to='data_waterfalls'),
        ),
    ]
