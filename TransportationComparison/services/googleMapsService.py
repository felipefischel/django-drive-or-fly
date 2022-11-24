import googlemaps
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)


def getLongAndLat(address):
  geocode_result = gmaps.geocode(address)
  return geocode_result[0]['geometry']['location']



#units is seconds and meters
def getCarDurationAndDistance(startLatLongDict, endLatLongDict):
  distance_matrix_result =gmaps.distance_matrix(startLatLongDict,endLatLongDict)
  return {"duration":  distance_matrix_result['rows'][0]['elements'][0]['duration']['value'],
  "distance": distance_matrix_result['rows'][0]['elements'][0]['distance']['value']}





 #EXAMPLE COORDINATES        
#(28.5330881,-81.3316141),(28.4330881,-81.3316141)