# capture feed 
# capture_feed.py — run this once to save a real feed snapshot
import requests, os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

response = requests.get(
    "https://api.transport.nsw.gov.au/v2/gtfs/realtime/sydenytrains",
    headers={"Authorization": f"apikey {API_KEY}"}
)
response.raise_for_status()

with open("feed_snapshot.pb", "wb") as f:
    f.write(response.content)

print(f"Saved {len(response.content)} bytes")