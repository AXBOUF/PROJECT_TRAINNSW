"""
NSW Trains Realtime Data Fetcher
Focused on understanding the data structure
Uses ?debug=true to get text format (no protobuf needed!)
"""
import requests
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")

# -----------------------------
# 1. FETCH THE DATA
# -----------------------------
print("🚂 Fetching NSW Trains realtime data...")

url = "https://api.transport.nsw.gov.au/v1/gtfs/realtime/nswtrains?debug=true"
headers = {"Authorization": f"apikey {API_KEY}"}

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    exit()

# -----------------------------
# 2. PARSE TEXT FORMAT
# -----------------------------
text = response.text

# Split into entities
entities = text.split("entity {")[1:]  # Skip header
print(f"📊 Found {len(entities)} trip updates\n")

# Prepare rows for CSV
rows = []

# Helper to extract value from text
def extract(pattern, text, default=""):
    match = re.search(pattern, text)
    return match.group(1) if match else default

for entity_text in entities:
    # Entity ID
    entity_id = extract(r'id: "([^"]*)"', entity_text)
    
    # Trip info
    trip_id = extract(r'trip_id: "([^"]*)"', entity_text)
    route_id = extract(r'route_id: "([^"]*)"', entity_text)
    start_time = extract(r'start_time: "([^"]*)"', entity_text)
    start_date = extract(r'start_date: "([^"]*)"', entity_text)
    
    # Find all stop_time_update blocks
    stop_blocks = entity_text.split("stop_time_update {")[1:]
    
    for stop_text in stop_blocks:
        stop_id = extract(r'stop_id: "([^"]*)"', stop_text)
        stop_sequence = extract(r'stop_sequence: (\d+)', stop_text, "0")
        
        # Arrival info
        arrival_delay = extract(r'arrival {\s*delay: (-?\d+)', stop_text, "0")
        arrival_time = extract(r'arrival {[^}]*time: (\d+)', stop_text, "0")
        
        # Departure info  
        departure_delay = extract(r'departure {\s*delay: (-?\d+)', stop_text, "0")
        departure_time = extract(r'departure {[^}]*time: (\d+)', stop_text, "0")
        
        # Convert to numbers
        arrival_delay = int(arrival_delay)
        departure_delay = int(departure_delay)
        delay_mins = round(arrival_delay / 60, 1)
        
        # Add row
        rows.append({
            "entity_id": entity_id,
            "trip_id": trip_id,
            "route_id": route_id,
            "start_time": start_time,
            "start_date": start_date,
            "stop_id": stop_id,
            "stop_sequence": int(stop_sequence),
            "arrival_delay_sec": arrival_delay,
            "arrival_delay_min": delay_mins,
            "arrival_time": arrival_time,
            "departure_delay_sec": departure_delay,
            "departure_time": departure_time,
            "fetched_at": datetime.now().isoformat()
        })

print(f"📝 Extracted {len(rows)} stop updates")

# -----------------------------
# 4. SHOW SAMPLE (terminal only, no CSV)
# -----------------------------
print("\n--- First 10 rows ---\n")
print(f"{'Trip ID':<20} {'Route':<15} {'Stop':<12} {'Delay (min)':<12}")
print("-" * 60)

for row in rows[:10]:
    delay_str = f"{row['arrival_delay_min']:+.1f}" if row['arrival_delay_min'] != 0 else "On time"
    print(f"{row['trip_id']:<20} {row['route_id']:<15} {row['stop_id']:<12} {delay_str:<12}")

print("\n--- Last 10 rows ---\n")
print(f"{'Trip ID':<20} {'Route':<15} {'Stop':<12} {'Delay (min)':<12}")
print("-" * 60)

for row in rows[-10:]:
    delay_str = f"{row['arrival_delay_min']:+.1f}" if row['arrival_delay_min'] != 0 else "On time"
    print(f"{row['trip_id']:<20} {row['route_id']:<15} {row['stop_id']:<12} {delay_str:<12}")

# -----------------------------
# 5. QUICK STATS
# -----------------------------
if rows:
    delays = [r['arrival_delay_min'] for r in rows]
    late = [d for d in delays if d > 1]
    early = [d for d in delays if d < -1]
    
    print(f"\n--- Quick Stats ---")
    print(f"Total stop updates: {len(rows)}")
    print(f"Running late (>1 min): {len(late)}")
    print(f"Running early (<-1 min): {len(early)}")
    print(f"Max delay: {max(delays):.1f} min")
    print(f"Avg delay: {sum(delays)/len(delays):.1f} min")
