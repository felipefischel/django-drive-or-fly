from urllib.request import urlopen
from amadeus import Client, ResponseError
import ssl
from django.conf import settings
import json
import re

#only  needed for running  the api call locally
def ssl_disabled_urlopen(endpoint):
    context = ssl._create_unverified_context()
    return urlopen(endpoint, context=context)


amadeus = Client(
    hostname='production',
    client_id=settings.AMADEUS_API_KEY,
    client_secret=settings.AMADEUS_API_SECRET,
    http=ssl_disabled_urlopen
)

#date formaat is YYYY-MM-DD
#currency is EURO
def getFlights(startPlace, destination,  date):
  try:
    response = amadeus.shopping.flight_offers_search.get(
        originLocationCode=startPlace,
        destinationLocationCode=destination,
        departureDate=date,
        adults=1)
    flights = map(getFlightInformation, response.data[0]['itineraries'][0]['segments'] )
    listOfFlights = list(flights)
    duration = response.data[0]['itineraries'][0]['duration']
    hours = formatDuration(duration)

    return {
      "totalPrice":response.data[0]['price']['grandTotal'],
      "flights":listOfFlights,
      "duration":hours
    }

  except:
    return {
      "totalPrice":-1,
      "flights":list(),
      "duration":-1
    }


def getAirports(lat, long):
  response =  amadeus.reference_data.locations.airports.get(
    longitude=long,
    latitude=lat)

  airportCodes = map(getAirportCode, response.data)

  return list(airportCodes)






def getAirportCode(airportInfo):
  return airportInfo['iataCode']

#flight times are format YYYY-MM-DDTHH:MM:SS in military time
def getFlightInformation(flight):
  return {
    "departureAirport": flight['departure']['iataCode'],
    "departureTime": flight['departure']['at'],
    "arrivalAirport": flight['arrival']['iataCode'],
    "arrivalTime": flight['arrival']['at'],
   "carrierCode": getCarrierName(flight['carrierCode'])
  }

def getCarrierName(carrierCode):
    jsonReader = open('TransportationComparison/static/TransportationComparison/data/airlines.json')
    carrierData = json.load(jsonReader)
    return carrierData[carrierCode]['Description']


def formatDuration(duration):
  h, m = re.findall('PT(\d+)H(\d+)M',duration)[0]
  return int(h) + float(m)/60



#EXAMPLE API CALLS:

#https://api.flightapi.io/roundtrip/6338e52003fdff3db04ceabd/LHR/LAX/2019-10-11/2019-10-15/2/0/1/Economy/USD


#{'lat': 28.5317408697085, 'lng': -81.3328855802915}

#https://api.flightapi.io/onewaytrip/6338e52003fdff3db04ceabd/LHR/LAX/2019-10-11/2/0/1/Economy/USD
