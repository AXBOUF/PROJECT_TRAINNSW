# NSW Transport Open Data - Getting Started Guide

A beginner-friendly guide to building apps with NSW Transport data.

---

## 🎯 Quick Overview

NSW Transport provides **free data** to build transport apps. There are two types:

| Type | What It Is | Format | Use Case |
|------|-----------|--------|----------|
| **Static Data** | Schedules, stops, routes | CSV/ZIP | "When does bus 333 run?" |
| **Realtime Data** | Live positions, delays | Protobuf | "Where is my bus right now?" |

---

## 📦 The Main Datasets

### Static Data (Download Once)

| Dataset | What's Inside | Update Frequency |
|---------|--------------|------------------|
| **Timetables Complete GTFS** | All schedules, stops, routes for ALL operators | Nightly |
| **Timetables For Realtime** | Schedules only for operators with realtime feeds | Nightly |
| **Location Facilities** | Station amenities (parking, bike racks, accessibility) | Periodic |

### Realtime Data (Fetch Often)

| Dataset | What's Inside | Update Frequency |
|---------|--------------|------------------|
| **Vehicle Positions** | Where buses/trains/ferries are NOW | Every 10-30 seconds |
| **Trip Updates** | Delays, cancellations, changed stops | Every 10-30 seconds |
| **Alerts** | Service disruptions, incidents | As they happen |

---

## 🚀 Step 1: Get Your API Key

1. Go to [opendata.transport.nsw.gov.au](https://opendata.transport.nsw.gov.au)
2. Click **Register** (top right)
3. Create an account
4. Go to your profile → **Applications** → Create new app
5. Copy your **API Key**

### Free Tier Limits
- **60,000 API calls/day**
- **5 requests/second**

> 💡 This is plenty! Realtime data only updates every 10-30 seconds anyway.

---

## 🔑 Step 2: Make Your First API Call

### Authentication
Add this header to ALL requests:
```
Authorization: apikey YOUR_API_KEY_HERE
```

### Example: Download Static GTFS
```python
import requests

API_KEY = "your_api_key_here"
url = "https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs"

response = requests.get(url, headers={"Authorization": f"apikey {API_KEY}"})

# Save the ZIP file
with open("gtfs_timetables.zip", "wb") as f:
    f.write(response.content)
```

### Example: Get Realtime Bus Positions
```python
import requests
import gtfs_realtime_pb2  # You need to generate this from proto file

API_KEY = "your_api_key_here"
url = "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses"

response = requests.get(url, headers={"Authorization": f"apikey {API_KEY}"})

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)
```

---

## 📁 What's in the GTFS ZIP File?

When you download the static GTFS, you get these files:

```
gtfs_data/
├── agency.txt        → Who runs the services (Sydney Buses, etc.)
├── routes.txt        → Route info (333, T1, F1, etc.)
├── stops.txt         → All stop locations (lat/lng)
├── trips.txt         → Individual journeys
├── stop_times.txt    → Arrival/departure at each stop
├── calendar.txt      → Which days services run
├── calendar_dates.txt→ Exceptions (holidays)
└── shapes.txt        → GPS points to draw routes on map
```

### How Files Connect

```
agency.txt ──► routes.txt ──► trips.txt ──► stop_times.txt
                                │                 │
                                └── shapes.txt    └── stops.txt
                                
trips.txt ──► calendar.txt (which days it runs)
```

---

## 🔴 Working with Realtime Data

Realtime feeds use **Protocol Buffers** (protobuf), not JSON/CSV.

### Step 1: Get the Proto File
Download from: [TfNSW GTFS-R Proto File](https://opendata.transport.nsw.gov.au)

### Step 2: Generate Python Code
```bash
pip install protobuf
protoc --python_out=. gtfs-realtime.proto
```

### Step 3: Parse the Feed
```python
import gtfs_realtime_pb2

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

for entity in feed.entity:
    if entity.HasField('vehicle'):
        print(f"Vehicle {entity.vehicle.vehicle.id}")
        print(f"  Position: {entity.vehicle.position.latitude}, {entity.vehicle.position.longitude}")
```

---

## 🌐 API Endpoints Reference

### Static GTFS (Download Daily Max)
| Endpoint | Description |
|----------|-------------|
| `/v1/publictransport/timetables/complete/gtfs` | All operators (ZIP) |
| `/v1/gtfs/schedule/buses` | Buses only |
| `/v1/gtfs/schedule/sydneytrains` | Sydney Trains only |
| `/v1/gtfs/schedule/ferries` | Ferries only |

### Realtime Vehicle Positions (Fetch every 10-15 sec)
| Endpoint | Description |
|----------|-------------|
| `/v1/gtfs/vehiclepos/buses` | All bus positions |
| `/v1/gtfs/vehiclepos/sydneytrains` | Train positions |
| `/v1/gtfs/vehiclepos/ferries` | Ferry positions |
| `/v1/gtfs/vehiclepos/lightrail` | Light rail positions |

### Realtime Trip Updates (Delays)
| Endpoint | Description |
|----------|-------------|
| `/v1/gtfs/realtime/buses` | Bus delays/changes |
| `/v1/gtfs/realtime/sydneytrains` | Train delays |
| `/v1/gtfs/realtime/ferries` | Ferry delays |

### Realtime Alerts
| Endpoint | Description |
|----------|-------------|
| `/v1/gtfs/alerts/buses` | Bus alerts |
| `/v1/gtfs/alerts/sydneytrains` | Train alerts |
| `/v1/gtfs/alerts/ferries` | Ferry alerts |

### Trip Planner APIs
| Endpoint | Description |
|----------|-------------|
| `/v1/tp/stop_finder` | Find stops by name |
| `/v1/tp/trip` | Plan a journey A→B |
| `/v1/tp/departure_mon` | Departures from a stop |
| `/v1/tp/add_info` | Service alerts |
| `/v1/tp/coord` | Find stops near coordinates |

---

## ⏰ How Often to Fetch Data?

| Data Type | How Often | Why |
|-----------|----------|-----|
| Static GTFS | Once per day | Updates nightly |
| Vehicle Positions | Every 10-15 seconds | Updates every 10 sec |
| Trip Updates | Every 10-15 seconds | Updates every 10 sec |
| Alerts | Every 30-60 seconds | Updates as needed |

> ⚠️ Don't fetch more often than data updates - you'll waste API calls!

---

## 🔗 Matching Static + Realtime Data

The **key insight**: Static and realtime data use **different IDs**!

To connect them:
1. Use the "Timetables For Realtime" GTFS (not the complete one)
2. Match `trip_id` from realtime feed to `trip_id` in static data
3. Check the [Reference Tables](https://opendata.transport.nsw.gov.au) for agency mappings

```python
# Realtime feed gives you:
trip_id = "123.456.789"

# Look up in static trips.txt to get:
route_id, service_id, trip_headsign, etc.
```

---

## 🛠️ Quick Start Checklist

- [ ] Register at [opendata.transport.nsw.gov.au](https://opendata.transport.nsw.gov.au)
- [ ] Create an application to get API key
- [ ] Download static GTFS and explore the CSV files
- [ ] Install `protobuf` Python package
- [ ] Generate Python code from proto file
- [ ] Make your first realtime API call
- [ ] Join the [Open Data Forum](https://opendata.transport.nsw.gov.au/forum) for help

---

## 📚 Official Documentation

| Document | What It Covers |
|----------|---------------|
| [GTFS Release Notes](https://opendata.transport.nsw.gov.au/sites/default/files/2023-08/TfNSW_GTFS_release_notes_V_4_3_20200819.pdf) | How TfNSW uses GTFS |
| [Buses Technical Doc](https://opendata.transport.nsw.gov.au/sites/default/files/2024-10/TfNSW_Realtime_Bus_Technical_Doc_v4.4.pdf) | Bus-specific details |
| [Sydney Trains Technical Doc](https://opendata.transport.nsw.gov.au/sites/default/files/2024-12/Real%20Time%20Train%20Technical%20Document%20v3_6_open%20data_0.pdf) | Train-specific details |
| [Ferries Technical Doc](https://opendata.transport.nsw.gov.au/sites/default/files/2023-08/TfNSW_Realtime_Ferry_Technical_Doc.pdf) | Ferry-specific details |
| [Trip Planner API Manual](https://opendata.transport.nsw.gov.au/sites/default/files/2023-08/Trip%20Planner%20API%20manual-opendataproduction%20v3.2.pdf) | Journey planning APIs |

---

## 💡 Pro Tips

1. **Start with static data** - easier to understand before tackling realtime
2. **Use the Trip Planner API** for quick journey planning (no protobuf needed!)
3. **Cache static data locally** - don't re-download every time your app runs
4. **Check `Last-Modified` header** to know if data has changed
5. **Join the Forum** - other devs are helpful and share code samples

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| 401 Unauthorized | Check API key format: `apikey YOUR_KEY` (with space) |
| Empty realtime feed | Some modes have no vehicles at night |
| IDs don't match | Use "For Realtime" GTFS, not "Complete" GTFS |
| Protobuf errors | Make sure you generated Python code from proto file |
| Rate limited | You're calling too fast, wait 10+ seconds between calls |

---

## 🎯 What to Build First?

**Easiest → Hardest:**

1. **Departure Board** - Show next buses at a stop (Trip Planner API, no protobuf)
2. **Route Viewer** - Display route on map (Static GTFS only)
3. **Live Map** - Show moving vehicles (Realtime + protobuf)
4. **Delay Tracker** - Compare scheduled vs actual (Static + Realtime)
5. **Full Trip Planner** - Complete journey planning app

---

*Last updated: March 2026*
