from urllib.request import urlopen
from amadeus import Client, ResponseError
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

#only  needed for running  the api call locally
def ssl_disabled_urlopen(endpoint):
    context = ssl._create_unverified_context()
    return urlopen(endpoint, context=context)


amadeus = Client(
    client_id=os.getenv("AMADEUS_API_KEY"),
    client_secret=os.getenv("AMADEUS_API_SECRET"),
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
   

    return {
      "totalPrice":response.data[0]['price']['grandTotal'],
      "flights":list(flights)
    }
    
  except ResponseError as error:
    print(error)


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
    "arrivlAirport": flight['arrival']['iataCode'],
    "arrivalTime": flight['arrival']['at'],
    "carrierCode": flight['carrierCode']
  }




#EXAMPLE API CALLS:

#https://api.flightapi.io/roundtrip/6338e52003fdff3db04ceabd/LHR/LAX/2019-10-11/2019-10-15/2/0/1/Economy/USD


#{'lat': 28.5317408697085, 'lng': -81.3328855802915}

#https://api.flightapi.io/onewaytrip/6338e52003fdff3db04ceabd/LHR/LAX/2019-10-11/2/0/1/Economy/USD
