"""
Test all NSW Transport Realtime API endpoints
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.transport.nsw.gov.au/v1/gtfs/realtime"

# All available endpoints from getrealtime_8.0.yaml
ENDPOINTS = {
    "Buses": "/buses",
    "Sydney Ferries": "/ferries/sydneyferries",
    "MFF Ferries": "/ferries/MFF",
    "Light Rail CBD & Southeast": "/lightrail/cbdandsoutheast",
    "Light Rail Newcastle": "/lightrail/newcastle",
    "Light Rail Parramatta": "/lightrail/parramatta",
    "NSW Trains": "/nswtrains",
}

headers = {"Authorization": f"apikey {API_KEY}"}

print("=" * 60)
print("NSW TRANSPORT REALTIME API TESTER")
print("=" * 60)

for name, endpoint in ENDPOINTS.items():
    url = BASE_URL + endpoint + "?debug=true"  # debug=true gives readable text
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Count how many entities (vehicles/updates) in response
            content = response.text
            entity_count = content.count("entity {")
            status = f"✅ OK - {entity_count} entities"
        else:
            status = f"❌ Error {response.status_code}"
            
    except requests.exceptions.Timeout:
        status = "⏱️ Timeout"
    except Exception as e:
        status = f"❌ {str(e)[:30]}"
    
    print(f"{name:30} {status}")

print("=" * 60)

# Detailed preview of one endpoint
print("\n📍 SAMPLE: Buses (first 5 entities)\n")

url = BASE_URL + "/buses?debug=true"
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # Split by entities and show first 5
    lines = response.text.split("entity {")
    for i, entity in enumerate(lines[1:6], 1):  # Skip header, show 5
        print(f"--- Entity {i} ---")
        # Clean up and show key info
        preview = entity[:500].strip()
        print(preview)
        print()
else:
    print(f"Error: {response.status_code}")
