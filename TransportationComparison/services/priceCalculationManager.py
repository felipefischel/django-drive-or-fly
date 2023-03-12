from .flightApiService import getAirports, getFlights
from .gasApiService import getGasPricesByUSState, getGasPricesByCoordinates
from .googleMapsService import getCarDurationAndDistance, getLongAndLat, getGeoCodeResult, getCountry, getUSState




def calculateCarCostAndDistanceAndDuration(start_geocode_result, end_geocode_result,queue):
   startLongLat  = getLongAndLat(start_geocode_result)
   endLongLat  =  getLongAndLat(end_geocode_result)
   if startLongLat['lat'] == "N/A" or endLongLat['lat'] == "N/A":
      retval = {"duration": -1, "distance":-1, "cost":-1, "gas_price": -1}
      queue.put(retval)
      return retval
   
   result =  getCarDurationAndDistance((startLongLat['lat'],startLongLat['lng']),(endLongLat['lat'],endLongLat['lng']))
   gallons = (float(result['distance'])/1000)/38.94
   country = getCountry(start_geocode_result)
   if country == 'US':
      state = getUSState(start_geocode_result)
      costPerGallon = getGasPricesByUSState(state)
   else:
      costPerGallon = getGasPricesByCoordinates(startLongLat['lng'],startLongLat['lat'])
   cost = float(costPerGallon)*gallons
   retval = {"duration": result['duration'], "distance":result['distance'], "cost":cost, "gas_price": costPerGallon}
   queue.put(retval)
   return retval

   #https://afdc.energy.gov/data/10310
   #avg mpg = 24.2
   #avg kpg = 38.94612


def calculateFlightCostAndHours(start_geo_code, end_geo_code, date,queue):
    startLongLat  = getLongAndLat(start_geo_code)
    endLongLat  =  getLongAndLat(end_geo_code)
    if startLongLat['lat'] == "N/A" or endLongLat['lat'] == "N/A":
      return {
      "totalPrice":-1,
      "flights":list(),
      "duration":-1
    }
   
    startAirport = getAirports(startLongLat['lat'],startLongLat['lng'])[0]
    endAirport = getAirports(endLongLat['lat'],endLongLat['lng'])[0]
    flights = getFlights(startAirport, endAirport,date)
    queue.put(flights)
    return flights
