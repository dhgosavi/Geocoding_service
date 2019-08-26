#Geocoding service
#Given latitude, longitude will return address of the location
import requests
from flask import Flask
from flask import request
from flask import abort
import json
import re

app = Flask(__name__)

#http://127.0.0.1:5000/login?latlng=40.714224,-73.961452
def google_service(latlng):
    params = dict()
    params["key"] = "<developer_key>"
    params["latlng"] =latlng
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return None

def here_service(latlng):
    params = dict()
    params["app_id"] = "<developer_app_id>"
    params["app_code"] = "<developer_app_code>"
    params["mode"] = "retrieveAddresses"
    params["maxresults"] = 1
    params["prox"] = latlng 
    base_url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?"
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        result_resp =  json.loads(response.content)
        return result_resp 
    else:
        return None

@app.route('/badrequest400')
def badrequest():
    abort(400)

@app.route('/serviceunavailable503')
def serviceunavailable():
    abort(503)

@app.route('/login', methods=['GET'])
def login():
    latlng = request.args.get('latlng')
    #Validate lat , lng entered by User
    lat, lng = str(latlng).split(",")
    z = re.match("^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$", lat)
    if not z:
        badrequest()
    z = re.match("^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$", lng)
    if not z:
        badrequest()
    resources = ["https://maps.googleapis.com/maps/api/geocode/json?", "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?"]
    
    #Geocoding service dictionary mapping resource to api
    geoservice_dict = {}    
    geoservice_dict[resources[0]] = google_service(latlng)
    geoservice_dict[resources[1]] = here_service(latlng)

    i=0
    while i < len(geoservice_dict):
        result = geoservice_dict[resources[i]]
        if result != None:
            return result
            break
        else:
            i+=1
    serviceunavailable()