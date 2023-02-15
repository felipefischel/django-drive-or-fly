import googlemaps
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def getLongAndLat(address):
  geocode_result = gmaps.geocode(address)
  if geocode_result:
    return geocode_result[0]['geometry']['location']

  return {"lat":"N/A"}



#units is seconds and meters
def getCarDurationAndDistance(startLatLongDict, endLatLongDict):
  try:
    distance_matrix_result =gmaps.distance_matrix(startLatLongDict,endLatLongDict)
    if(distance_matrix_result['rows'][0]['elements'][0]['status']=='ZERO_RESULTS'):
      return {"duration":  -1,"distance":-1} 
    
    return {"duration":  distance_matrix_result['rows'][0]['elements'][0]['duration']['value'],
    "distance": distance_matrix_result['rows'][0]['elements'][0]['distance']['value']}
  except:
    return {"duration":  -1,"distance":-1}





 #EXAMPLE COORDINATES        
#(28.5330881,-81.3316141),(28.4330881,-81.3316141)