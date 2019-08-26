#Geocoding service
#Given latitude, longitude will return address of the location

import requests
from flask import Flask
from flask import request
import json
import pprint
import re
#http://127.0.0.1:5000/login?latlng=40.714224,-73.961452

app = Flask(__name__)
@app.route('/login', methods=['GET'])
def login():
    latlng = request.args.get('latlng')
    #Validate lat , lng entered by User
    lat, lng = str(latlng).split(",")
    z = re.match("^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[0-9]|[1-8][0-9])(?:(?:\.[0-9]{1,6})?))$", lat)
    if not z:
        print("Invalid Latitude")
        return "Invalid Latitude"
    z = re.match("^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[0-9]|[1-9][0-9]|1[0-7][0-9])(?:(?:\.[0-9]{1,6})?))$", lng)
    if not z:
        print("Invalid Longitude")
        return "Invalid Longitude"
    
    base_url = "https://maps.googleapis.com/maps/api/geocode/json?"
    params = dict()
    #Enter developer key
    params["key"] = "<developerkey>"
    params["latlng"] =latlng
    response = requests.get(base_url, params=params).content
    result_resp =  json.loads(response)
    if str(result_resp["status"]) != "OK":
        #try back up service
        print("Trying backup service")
        backup_url = "https://reverse.geocoder.api.here.com/6.2/reversegeocode.json?"
        #Enter developer app_id and app_code
        params["app_id"] = "<developer_api_id"
        params["app_code"] = "developer_app_code"
        params["mode"] = "retrieveAddresses"
        params["maxresults"] = 1
        params["prox"] = latlng 
        response = requests.get(base_url, params=params).content
        result_resp =  json.loads(response)
        return result_resp
    else:
        return result_resp