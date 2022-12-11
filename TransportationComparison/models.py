from django.db import models


class Flight(models.Model):
  starting_airport_code = models.CharField(max_length = 500)
  destination_airport_code = models.CharField(max_length = 500)
  departure = models.DateTimeField()
  arrival = models.DateTimeField()
  airline_code = models.CharField(max_length = 500)

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
  flights = models.ManyToManyField(Flight)

  