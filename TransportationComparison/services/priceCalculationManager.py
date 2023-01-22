from .flightApiService import getAirports, getFlights
from .gasApiService import getGasPricesByUSState
from .googleMapsService import getCarDurationAndDistance, getLongAndLat



def calculateCarCostAndDistanceAndDuration(start, end):
   startLongLat  = getLongAndLat(start)
   endLongLat  =  getLongAndLat(end)
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
    startAirport = getAirports(startLongLat['lat'],startLongLat['lng'])
    endAirport = getAirports(endLongLat['lat'],endLongLat['lng'])
    return getFlights(startAirport, endAirport,date)
