# Generated by Django 1.11.20 on 2019-05-03 23:04

from django.db import migrations, models


def populate_transmitter_mode_name(apps, schema_editor):
    Observation = apps.get_model('base', 'Observation')
    observations = Observation.objects.all()
    for observation in observations:
        if observation.transmitter_mode is not None:
            observation.transmitter_mode_name = observation.transmitter_mode.name
            observation.save()

def reverse_populate_transmitter_mode_name(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('base', '0058_add_transmitter_into_observation_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='observation',
            name='transmitter_mode_name',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.RunPython(populate_transmitter_mode_name, reverse_populate_transmitter_mode_name),
        migrations.RemoveField(
            model_name='observation',
            name='transmitter_mode',
        ),
        migrations.DeleteModel(
            name='Mode',
        ),
        migrations.RenameField(
            model_name='observation',
            old_name='transmitter_mode_name',
            new_name='transmitter_mode',
        ),
    ]
