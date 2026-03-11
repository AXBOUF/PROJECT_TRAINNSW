from google.protobuf.json_format import MessageToDict
import gtfs_realtime_pb2
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")

# GTFS-Realtime endpoints (choose one)
ENDPOINTS = {
    "bus_positions": "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses",
    "train_positions": "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/sydneytrains",
    "ferry_positions": "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/ferries",
    "bus_updates": "https://api.transport.nsw.gov.au/v1/gtfs/realtime/buses",
    "train_updates": "https://api.transport.nsw.gov.au/v1/gtfs/realtime/sydneytrains",
    "bus_alerts": "https://api.transport.nsw.gov.au/v1/gtfs/alerts/buses",
}

# Select which feed to fetch
selected = "bus_positions"
url = ENDPOINTS[selected]

print(f"Fetching: {selected}")
print(f"URL: {url}\n")

response = requests.get(url, headers={"Authorization": f"apikey {API_KEY}"})

if response.status_code == 200:
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)
    
    data = MessageToDict(feed)
    
    # Show feed header
    header = data.get("header", {})
    timestamp = header.get("timestamp")
    if timestamp:
        print(f"Feed timestamp: {datetime.fromtimestamp(int(timestamp))}")
    print(f"GTFS Realtime version: {header.get('gtfsRealtimeVersion', 'N/A')}")
    
    # Show entities
    entities = data.get("entity", [])
    print(f"Total entities: {len(entities)}\n")
    
    # Preview first 3 entities
    print("--- First 3 entities ---")
    for i, entity in enumerate(entities[:3]):
        print(f"\nEntity {i+1}:")
        
        # Vehicle position
        if "vehicle" in entity:
            v = entity["vehicle"]
            pos = v.get("position", {})
            print(f"  Vehicle ID: {v.get('vehicle', {}).get('id', 'N/A')}")
            print(f"  Trip ID: {v.get('trip', {}).get('tripId', 'N/A')}")
            print(f"  Route ID: {v.get('trip', {}).get('routeId', 'N/A')}")
            print(f"  Latitude: {pos.get('latitude', 'N/A')}")
            print(f"  Longitude: {pos.get('longitude', 'N/A')}")
            print(f"  Speed: {pos.get('speed', 'N/A')} m/s")
        
        # Trip update (delays)
        if "tripUpdate" in entity:
            tu = entity["tripUpdate"]
            print(f"  Trip ID: {tu.get('trip', {}).get('tripId', 'N/A')}")
            print(f"  Route ID: {tu.get('trip', {}).get('routeId', 'N/A')}")
            stop_updates = tu.get("stopTimeUpdate", [])
            if stop_updates:
                print(f"  Stop updates: {len(stop_updates)}")
        
        # Alert
        if "alert" in entity:
            alert = entity["alert"]
            print(f"  Alert: {alert.get('headerText', {}).get('translation', [{}])[0].get('text', 'N/A')}")

else:
    print(f"Error: {response.status_code}")
    print(response.text)
