# NSW Transport GTFS Data - Overview

## What GTFS Data Is For

**Yes, this data is used for trip planning!** Apps like Google Maps, Citymapper, and TripView use this exact data format.

| Data File | Purpose | Trip Planning Use |
|-----------|---------|-------------------|
| `stops.txt` | All stop locations | "Where can I catch a bus?" |
| `routes.txt` | Route info (501, T1, etc.) | "Which routes go to CBD?" |
| `trips.txt` | Individual journeys | "When does this bus leave?" |
| `stop_times.txt` | Arrival/departure times | "What time at each stop?" |
| `calendar.txt` | Which days service runs | "Does it run on weekends?" |
| `shapes.txt` | Route path on map | Drawing routes on a map |

## How Often Is It Updated?

NSW Transport updates this static data:
- **Regular updates**: Usually **weekly** or when schedules change
- **Major updates**: When new routes/timetables are introduced

To check if there's new data, use the `Last-Modified` header:
```python
response = requests.head(url, headers={"Authorization": f"apikey {API_KEY}"})
print(response.headers.get("Last-Modified"))
```

## Data Currency

As of March 11, 2026:

| Field | Value |
|-------|-------|
| **Start Date** | `20260311` (March 11, 2026) |
| **End Date** | Up to `20260609` (June 9, 2026) |

## Static vs Realtime - The Full Picture

```
┌─────────────────────────────────────────────────────────┐
│                    TRIP PLANNING                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   STATIC GTFS (you have this)     GTFS-REALTIME        │
│   ─────────────────────────       ─────────────        │
│   • Planned schedules             • Actual positions   │
│   • "Bus should arrive 3:15pm"    • "Bus is here now"  │
│   • Updated weekly                • Updated every 15s  │
│                                                         │
│            ↓                              ↓             │
│   ┌─────────────────────────────────────────────────────┐
│   │        TRIP PLANNING APPS COMBINE BOTH              │
│   │   "Bus 501 scheduled 3:15pm, running 2 min          │
│   │    late, currently at George St"                    │
│   └─────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────┘
```

## Summary

| Question | Answer |
|----------|--------|
| Is this for trip planning? | ✅ Yes, exactly what apps use |
| Is your data recent? | ✅ Yes, starts today (March 11, 2026) |
| Does it match real trips? | ✅ It's the **planned** schedule; combine with realtime for actual |
| How often to re-download? | Weekly, or check `Last-Modified` header |

## API Endpoints

### Static GTFS (download once)
```
https://api.transport.nsw.gov.au/v1/publictransport/timetables/complete/gtfs
```

### GTFS-Realtime (fetch frequently)
```
# Vehicle Positions
https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses
https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/sydneytrains
https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/ferries

# Trip Updates (delays)
https://api.transport.nsw.gov.au/v1/gtfs/realtime/buses
https://api.transport.nsw.gov.au/v1/gtfs/realtime/sydneytrains

# Alerts
https://api.transport.nsw.gov.au/v1/gtfs/alerts/buses
```
