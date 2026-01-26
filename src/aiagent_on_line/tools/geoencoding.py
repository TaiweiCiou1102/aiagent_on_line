import requests
import os
from dotenv import load_dotenv
load_dotenv()   

API_KEY = os.getenv("GOOGLE_GEOCODING_API_KEY")
API_URL = "https://maps.googleapis.com/maps/api/geocode/json"

def get_coordinates(address:str) -> tuple:
    params = {
        "address": address,
        "key": API_KEY
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    if data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        return location['lat'], location['lng']
    else:
        print("get_coordinates 失敗")
        print(data)
        return None, None
    

