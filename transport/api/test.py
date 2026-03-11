import requests 
import load_dotenv as dotenv
import os 

latitude = -33.8830
longitude = 151.2070

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://api.transport.nsw.gov.au/v1/tp/coord"
headers = {
    "Authorization": f"apikey {API_KEY}"
}
params = {
    "outputFormat": "rapidJSON",
    "coord": f"{latitude}:{longitude}",
    "type_1": "stop",   # we want transport stops
    "radius_1": "1500"  # in meters
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    print("Nearby stops:")
    for stop in data.get("locations", []):
        name = stop["name"]
        lat = stop["coord"]["lat"]
        lon = stop["coord"]["lon"]
        print(f"{name} -> {lat}, {lon}")
else:
    print("API request failed with status code:", response.status_code)