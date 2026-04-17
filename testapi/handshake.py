import requests 
import json 
from google.transit import gtfs_realtime_pb2 
from dotenv import load_dotenv
import os 

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://api.transport.nsw.gov.au/v2/gtfs/vehiclepos/sydneytrains"

headers = {
    "Authorization": f"apikey {API_KEY}"
}

response = requests.get(url, headers=headers)
if response.status_code == 200:
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    print(f"Number of vehicle positions: {len(feed.entity)}")
    for entity in feed.entity[:1]:  # Print first 1 for brevity
        print(f"Entity ID: {entity}")
#         if entity.HasField("vehicle"):
#             print(f"Vehicle ID: {entity.vehicle.vehicle.id}, Route: {entity.vehicle.trip.route_id}")
# else:    
#     print("API request failed with status code:", response.status_code)     
