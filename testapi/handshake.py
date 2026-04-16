import requests 
import json 
from google.transit import gtfs_realtime_pb2 
from google.protobuf.json_format import MessageToDict
from dotenv import load_dotenv
import os 

load_dotenv()
API_KEY = os.getenv("API_KEY")

url = "https://api.transport.nsw.gov.au/v2/gtfs/realtime/sydneytrains"

headers = {
    "Authorization": f"apikey {API_KEY}"
}

response = requests.get(url, headers=headers)

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

# ✅ Convert entire feed to dict
first = MessageToDict(feed.entity[0])

# ✅ Save to JSON
with open("testapi/feed.json", "w") as f:
    json.dump(first, f, indent=2)

