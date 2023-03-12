import http.client
import os
import json
from django.conf import settings



#returns $ per gallon
def getGasPricesByUSState(state):

  try:
    conn = http.client.HTTPSConnection("api.collectapi.com")
    
    headers = {
        'content-type': "application/json",
        'authorization': settings.COLLECT_API_KEY
    }
    
    conn.request("GET", "/gasPrice/stateUsaPrice?state="+state, headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    data_as_json = json.loads(data)

    return data_as_json['result']['state']['gasoline']
  
  except:
    return 3.217


#returns $ per gallon
def getGasPricesByCoordinates(long, lat):

  try:
    conn = http.client.HTTPSConnection("api.collectapi.com")
    
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 34W4lQPvSG3GDXJID7EBt0:1joGbDBEY89Sa00Ch8lUXo"
    }
    
    conn.request("GET", "/gasPrice/fromCoordinates?lng="+str(long)+"&lat="+str(lat), headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    data_as_json = json.loads(data)
    return data_as_json['result']['gasoline']
  
  except:
    return 3.217