# Generated by Django 3.2.13 on 2022-09-25 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TripInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starting_address', models.CharField(max_length=500)),
                ('destination_address', models.CharField(max_length=500)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TripOutput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_cost', models.FloatField()),
                ('flight_duration', models.FloatField()),
                ('drive_cost', models.FloatField()),
                ('drive_duration', models.FloatField()),
            ],
        ),
    ]
