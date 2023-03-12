import googlemaps
from django.conf import settings

gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)

def getGeoCodeResult(address):
  return gmaps.geocode(address)
  

def getLongAndLat(geocode_result):
  if geocode_result:
    return geocode_result[0]['geometry']['location']

  return {"lat":"N/A"}



def getCountry(geocode_result):
  components = geocode_result[0]['address_components']
  country_component= filter(lambda component: checkGeocodeComponent(component,"country"),components)
  country_component_list = list(country_component)
  if len(country_component_list) == 1:
    return country_component_list[0]['short_name']
  return "N/A"

def getUSState(geocode_result):
  components = geocode_result[0]['address_components']
  country_component= filter(lambda component: checkGeocodeComponent(component,"administrative_area_level_1"),components)
  country_component_list = list(country_component)
  if len(country_component_list) == 1:
    return country_component_list[0]['short_name']
  return "N/A"


def checkGeocodeComponent(component, type):
  if type in component['types']:
    return True
  return False


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