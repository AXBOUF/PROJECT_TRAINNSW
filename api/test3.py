from google.protobuf.json_format import MessageToDict
import gtfs_realtime_pb2
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("API_KEY")
url = "https://api.transport.nsw.gov.au/v1/gtfs/realtime/"

'''
Operations: to choose from https://opendata.transport.nsw.gov.au/data/dataset/public-transport-realtime-trip-update/resource/d936a1c6-1fe6-4985-9df2-326e91036f80
GET /sydneytrains - Note - this feed has been superseded by version 2
GET /buses
GET /ferries/
GET /lightrail/
GET /lightrail/innerwest - Note - this feed has been superseded by version 2
GET /nswtrains
GET /regionbuses/
GET /metro - Note - this feed has been superseded by version 2
'''


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
