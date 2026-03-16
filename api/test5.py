# mock_trip.py — your test harness
import gtfs_realtime_pb2
from google.protobuf.json_format import MessageToDict

def load_feed(path="feed_snapshot.pb"):
    feed = gtfs_realtime_pb2.FeedMessage()
    with open(path, "rb") as f:
        feed.ParseFromString(f.read())
    return MessageToDict(feed)

def get_trip_updates(feed_dict):
    """Extract all trip updates with delay info."""
    updates = []
    for entity in feed_dict.get("entity", []):
        tu = entity.get("tripUpdate")
        if not tu:
            continue
        trip = tu.get("trip", {})
        stops = tu.get("stopTimeUpdate", [])
        updates.append({
            "entity_id":  entity.get("id"),
            "trip_id":    trip.get("tripId"),
            "route_id":   trip.get("routeId"),
            "direction":  trip.get("directionId"),
            "start_time": trip.get("startTime"),
            "start_date": trip.get("startDate"),
            "stops":      stops,
        })
    return updates

def print_trip(trip):
    """Pretty-print one trip update — use this to verify your app's output."""
    print(f"\n{'─'*50}")
    print(f"  Trip ID   : {trip['trip_id']}")
    print(f"  Route     : {trip['route_id']}  Direction: {trip['direction']}")
    print(f"  Scheduled : {trip['start_date']} {trip['start_time']}")
    print(f"  Stops     : {len(trip['stops'])}")
    for stop in trip["stops"]:
        arr   = stop.get("arrival",   {}).get("delay", 0)
        dep   = stop.get("departure", {}).get("delay", 0)
        sched = stop.get("scheduleRelationship", "SCHEDULED")
        print(f"    [{stop.get('stopSequence','?'):>3}] stop {stop.get('stopId','?'):<8} "
              f"arr {arr:+4}s  dep {dep:+4}s  ({sched})")

# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    feed   = load_feed()
    trips  = get_trip_updates(feed)

    print(f"Feed has {len(trips)} trip updates")

    # --- filter to one specific trip to compare with your app ---
    TARGET_ROUTE = "T1"          # change to your route
    TARGET_TRIP  = None          # set to a specific tripId if you know it

    matches = [t for t in trips if TARGET_ROUTE in (t["route_id"] or "")]
    if TARGET_TRIP:
        matches = [t for t in matches if t["trip_id"] == TARGET_TRIP]

    print(f"Matched {len(matches)} trips for route '{TARGET_ROUTE}'")

    # Print first 3 matches so you can pick one to track
    for trip in matches[:3]:
        print_trip(trip)