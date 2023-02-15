from .flightApiService import getAirports, getFlights
from .gasApiService import getGasPricesByUSState
from .googleMapsService import getCarDurationAndDistance, getLongAndLat



def calculateCarCostAndDistanceAndDuration(start, end):
   startLongLat  = getLongAndLat(start)
   endLongLat  =  getLongAndLat(end)
   if startLongLat['lat'] == "N/A" or endLongLat['lat'] == "N/A":
      return {"duration": -1, "distance":-1, "cost":-1, "gas_price": -1}
   
   result =  getCarDurationAndDistance((startLongLat['lat'],startLongLat['lng']),(endLongLat['lat'],endLongLat['lng']))
   gallons = (float(result['distance'])/1000)/38.94
   costPerGallon = getGasPricesByUSState()
   cost = float(costPerGallon)*gallons
   return {"duration": result['duration'], "distance":result['distance'], "cost":cost, "gas_price": costPerGallon}


   #https://afdc.energy.gov/data/10310
   #avg mpg = 24.2
   #avg kpg = 38.94612


def calculateFlightCostAndHours(start, end, date):
    startLongLat  = getLongAndLat(start)
    endLongLat  =  getLongAndLat(end)
    if startLongLat['lat'] == "N/A" or endLongLat['lat'] == "N/A":
      return {
      "totalPrice":-1,
      "flights":list(),
      "duration":-1
    }
   
    startAirport = getAirports(startLongLat['lat'],startLongLat['lng'])
    endAirport = getAirports(endLongLat['lat'],endLongLat['lng'])
    return getFlights(startAirport, endAirport,date)
