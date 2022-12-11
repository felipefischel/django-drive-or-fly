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




# Create your views here.


def Index(request):
    template = loader.get_template('TransportationComparison/index.html')
    form = TripForm()
    context = {'form':form}

    return HttpResponse(template.render(context, request))

def autocomplete(request):
    return render(request, 'googleMap.html', {'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY})


def Result(request, trip_output_id):
    try:
      trip = TripOutput.objects.get(pk=trip_output_id)
    except TripOutput.DoesNotExist:
      raise Http404("Trip does not exist")

    template = loader.get_template('TransportationComparison/result.html')
    print("bbbbbbb")
    print(trip.flights)
    #leemos la base de datos y la guardamos en una variable X
    context = {
        "flightDuration":trip.flight_duration,
        "driveDuration":trip.drive_duration,
        "flightCost":trip.flight_cost,
        "driveCost":trip.drive_cost,
        "flights":trip.flights.all()
    }
    return HttpResponse(template.render(context, request))


def Compare(request):
  # if this is a POST request we need to process the form data
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
            date_end = form.data['date_end']
            print(date_start)

    # if a GET (or any other method) we'll create a blank form
        else:
            return render(request, "TransportationComparison/index.html", {'form':form})
    else:
        form = TripForm(None)
        return render(request, "TransportationComparison/index.html", {'form':form})

    car_cost_and_distance = priceCalculationManager.calculateCarCostAndDistanceAndDuration(starting_destination,final_destination)
    flight_cost_and_distance  = priceCalculationManager.calculateFlightCostAndHours(starting_destination, final_destination,date_start)

    tripOutput = TripOutput(
      flight_cost=round(float(flight_cost_and_distance['totalPrice']),2),
      drive_cost=round(float(car_cost_and_distance['cost']),2),
      flight_duration=round(float(flight_cost_and_distance['duration']),2),
      drive_duration=round(float(car_cost_and_distance['duration']/3600 ),2)
      )


    tripOutput.save()
    print("111111")
    print(flight_cost_and_distance)
    for flight in flight_cost_and_distance['flights']:
      print("aaaaaaaaaa")
      #datetime.strptime(a[0]['departureTime'],format_str).time()
      print(flight)
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

    


    return HttpResponseRedirect(reverse('comparison:result', args=(tripOutput.id, )))
