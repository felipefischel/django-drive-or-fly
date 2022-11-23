from django.db import models

# Create your models here.
class TripInput(models.Model):
  starting_address = models.CharField(max_length = 500) 
  destination_address = models.CharField(max_length = 500)
  start_date = models.DateField()
  end_date = models.DateField()


class TripOutput(models.Model):
  flight_cost = models.FloatField()
  flight_duration = models.FloatField()
  drive_cost = models.FloatField()
  drive_duration = models.FloatField()

  