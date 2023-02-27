from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import TripOutput, Flight
from django.http import Http404
import datetime
from .services import gasApiService
from .forms import TripForm
from django.conf import settings
from .services import priceCalculationManager
from django.template.response import TemplateResponse
from .utils import  dateUtils

# Create your views here.

def Index(request):
    template = loader.get_template('TransportationComparison/index.html')
    form = TripForm()
    backgroundimage = "url('https://drive.google.com/file/d/1ofqWqnfwzSzw_Ms-9dAy363nmqCiKeHr/view?usp=sharing')"
    #TODO: Make  backroundImage pull from an image from gcloud randomly
    context = {'form':form, 'backgroundimage': backgroundimage}
    return HttpResponse(template.render(context, request))

def About(request):
    template = loader.get_template('TransportationComparison/about.html')
    return HttpResponse(template.render({},request))

def autocomplete(request):
    return render(request, 'TransportationComparison/googleMap.html', {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})

def Result(request, trip_output_id):
    try:
      trip = TripOutput.objects.get(pk=trip_output_id)
    except TripOutput.DoesNotExist:
      raise Http404("Trip does not exist")

    template = loader.get_template('TransportationComparison/result.html')
    backgroundimage = "url('https://drive.google.com/file/d/1ofqWqnfwzSzw_Ms-9dAy363nmqCiKeHr/view?usp=sharing')"

    # Calculating the layover time
    seconds_in_layover = 0
    flights = trip.flights.all()
    flight_list = list(flights)
    if len(flight_list) >= 2:
        for i in range(0, len(flight_list) - 1):
            diff = flight_list[i+1].departure - flight_list[i].arrival
            seconds_in_layover = seconds_in_layover + diff.seconds

    hours_in_layover = seconds_in_layover/3600
    hours_flying = trip.flight_duration - hours_in_layover

    #leemos la base de datos y la guardamos en una variable X
    context = {
        "flightDuration":dateUtils.transformHoursFloatIntoTime(trip.flight_duration),
        "driveDuration": dateUtils.transformHoursFloatIntoTime(trip.drive_duration),
        "flightCost":round(float(trip.flight_cost),1),
        "driveCost":round(float(trip.drive_cost),1),
        "flights":trip.flights.all(),
        "driveDistance":round(float(trip.drive_distance),1),
        "gasPrice":round(float(trip.gas_price),1),
        "backgroundimage":backgroundimage,
        "carCO2Emissions":round(float(trip.drive_distance*0.1147),1),
        "flightCO2Emissions":round(float(hours_flying*125),1),
        "driveCarbonPrice":round(float(trip.drive_distance*0.1147*0.0363),1),
        "flightCarbonPrice":round(float(hours_flying*125*0.0363),1),
    }
    return HttpResponse(template.render(context, request))

def Compare(request):
    backgroundimage = "url('https://drive.google.com/file/d/1ofqWqnfwzSzw_Ms-9dAy363nmqCiKeHr/view?usp=sharing')"
    # Todo, Make  backroundImage pull from an image from gcloud randomly
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TripForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...

            starting_destination = form.data['starting_destination']
            final_destination = form.data['final_destination']
            date_start = form.data['date_start']

    # if a GET (or any other method) we'll create a blank form
        else:
            return render(request, "TransportationComparison/index.html", {'form':form, 'backgroundimage': backgroundimage})
    else:
        form = TripForm(None)
        return render(request, "TransportationComparison/index.html",{'form':form, 'backgroundimage': backgroundimage})

    car_cost_and_distance = priceCalculationManager.calculateCarCostAndDistanceAndDuration(starting_destination,final_destination)
    flight_cost_and_distance  = priceCalculationManager.calculateFlightCostAndHours(starting_destination, final_destination,date_start)

    tripOutput = TripOutput(
      flight_cost=round(float(flight_cost_and_distance['totalPrice']),2),
      drive_cost=round(float(car_cost_and_distance['cost']),2),
      flight_duration=round(float(flight_cost_and_distance['duration']),2),
      drive_duration=round(float(car_cost_and_distance['duration']/3600 ),2),
      drive_distance=round(float(car_cost_and_distance['distance']/1000),2),
      gas_price=round(float(car_cost_and_distance['gas_price']),2),
      )

    tripOutput.save()
    for flight in flight_cost_and_distance['flights']:
      flightModel = Flight(
        starting_airport_code=flight['departureAirport'],
        destination_airport_code=flight['arrivalAirport'],
        departure=flight['departureTime'],
        arrival=flight['arrivalTime'],
        airline_code=flight['carrierCode']
      )
      flightModel.save()
      tripOutput.flights.add(flightModel)
      tripOutput.save()

    return HttpResponseRedirect(reverse('comparison:result', args=( tripOutput.id, )))
