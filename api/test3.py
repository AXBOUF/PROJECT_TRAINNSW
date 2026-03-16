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
'''


response = requests.get(url, headers={"Authorization": f"apikey {API_KEY}"})
feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
feed_dict = MessageToDict(feed) 

