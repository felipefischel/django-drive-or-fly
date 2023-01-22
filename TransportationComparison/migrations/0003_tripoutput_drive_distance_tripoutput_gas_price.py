# Generated by Django 4.1.3 on 2023-01-22 18:00

from django.db import migrations, models

def update_data(apps, schema_editor):
    MyModel = apps.get_model("TransportationComparison", "tripoutput")
    for obj in MyModel.objects.all():
        obj.drive_distance = 0
        obj.gas_price = 0
        obj.save()


class Migration(migrations.Migration):

    dependencies = [
        ('TransportationComparison', '0002_flight_tripoutput_flights'),
    ]

    operations = [
        migrations.AddField(
            model_name='tripoutput',
            name='drive_distance',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='tripoutput',
            name='gas_price',
            field=models.FloatField(default=0),
        ),
        migrations.RunPython(update_data),
    ]
