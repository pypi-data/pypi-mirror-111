# Generated by Django 1.11.4 on 2017-09-09 13:26

from django.db import migrations


class Migration(migrations.Migration):

    def move_data(apps, schema_editor):
        Data = apps.get_model('base', 'Data')
        Observation = apps.get_model('base', 'Observation')
        DemodData = apps.get_model('base', 'DemodData')
        for observation in Observation.objects.all():
            obs = Observation.objects.filter(pk=observation.pk)
            data = Data.objects.filter(observation=observation)
            for counter, datum in enumerate(data):
                demod = DemodData.objects.filter(data=datum)
                obj = {
                    'satellite': datum.observation.satellite,
                    'transmitter': datum.observation.transmitter,
                    'tle': datum.observation.tle,
                    'author': datum.observation.author,
                    'start': datum.start,
                    'end': datum.end,
                    'ground_station': datum.ground_station,
                    'payload': datum.payload,
                    'waterfall': datum.waterfall,
                    'vetted_datetime': datum.vetted_datetime,
                    'vetted_user': datum.vetted_user,
                    'vetted_status': datum.vetted_status,
                    'rise_azimuth': datum.rise_azimuth,
                    'max_altitude': datum.max_altitude,
                    'set_azimuth': datum.set_azimuth
                }
                # this observation becomes its first data object
                if not counter:
                    obs.update(**obj)
                    obs_new = obs.get()
                # new observation objects for all the next data objects
                else:
                    obs_new = Observation.objects.create(**obj)
                demod.update(observation=obs_new)


    dependencies = [
        ('base', '0022_auto_20170909_2103'),
    ]

    operations = [
        migrations.RunPython(move_data),
    ]
