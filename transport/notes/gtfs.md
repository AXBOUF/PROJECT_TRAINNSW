# GTFS Data Files Reference

This document describes each file in the GTFS (General Transit Feed Specification) dataset from NSW Transport.

---

## 📊 File Overview

| File | Records | Description |
|------|---------|-------------|
| `agency.txt` | 709 | Transit agencies operating services |
| `stops.txt` | 170,052 | All stop/station locations |
| `routes.txt` | 10,173 | Bus/train/ferry routes |
| `trips.txt` | 193,922 | Individual scheduled trips |
| `stop_times.txt` | Very Large (50MB+) | Arrival/departure times at each stop |
| `calendar.txt` | 2,222 | Regular weekly service schedules |
| `calendar_dates.txt` | 32,938 | Service exceptions (holidays, etc.) |
| `shapes.txt` | Very Large (50MB+) | GPS coordinates for route paths |
| `notes.txt` | 811 | Special notes for trips |
| `levels.txt` | 9 | Station levels (platforms, concourse) |
| `pathways.txt` | 5,760 | Walking paths within stations |

---

## 📁 Detailed File Descriptions

### agency.txt
**Transit operators providing services**

| Column | Description | Example |
|--------|-------------|---------|
| `agency_id` | Unique agency identifier | `701` |
| `agency_name` | Agency name | `train replacement bus operators` |
| `agency_url` | Website | `http://transportnsw.info` |
| `agency_timezone` | Timezone | `Australia/Sydney` |
| `agency_lang` | Language | `EN` |
| `agency_phone` | Contact phone | (optional) |

**Sample:**
```
agency_id,agency_name,agency_url,agency_timezone,agency_lang,agency_phone
"701","train replacement bus operators","http://transportnsw.info","Australia/Sydney","EN",""
"25101","Special Event Buses","http://transportnsw.info","Australia/Sydney","EN",""
```

---

### stops.txt
**All stop and station locations**

| Column | Description | Example |
|--------|-------------|---------|
| `stop_id` | Unique stop identifier | `2000110` |
| `stop_code` | Public stop code | `2000110` |
| `stop_name` | Stop name | `Central Station, Forecourt, Coach Bay 5` |
| `stop_lat` | Latitude | `-33.88285863` |
| `stop_lon` | Longitude | `151.20471982` |
| `location_type` | 0=stop, 1=station | `` |
| `parent_station` | Parent station ID | `200060` |
| `wheelchair_boarding` | 0=unknown, 1=yes, 2=no | `1` |
| `level_id` | Station level | `Level 1` |
| `platform_code` | Platform number | `` |

**Sample:**
```
stop_id,stop_code,stop_name,stop_lat,stop_lon,location_type,parent_station,wheelchair_boarding,level_id,platform_code
"2000110","2000110","Central Grand Concourse, Light Rail Trackwork","-33.88222655","151.20634156","","200060","1","Level 1",""
"2000112","2000112","Central Station, Forecourt, Coach Bay 5","-33.88285863","151.20471982","","200060","2","Level 1",""
```

---

### routes.txt
**Route definitions (bus lines, train lines, etc.)**

| Column | Description | Example |
|--------|-------------|---------|
| `route_id` | Unique route identifier | `1-11B-M-sj2-1` |
| `agency_id` | Operating agency | `700` |
| `route_short_name` | Route number | `11BM` |
| `route_long_name` | Full route description | `Springwood, then all stations to Lithgow` |
| `route_desc` | Additional description | `Temporary buses` |
| `route_type` | Mode (see below) | `714` |
| `route_color` | Hex color | `00B5EF` |
| `route_text_color` | Text color | `FFFFFF` |
| `exact_times` | Fixed schedule | `1` |

**Route Types:**
| Code | Mode |
|------|------|
| 0 | Tram/Light Rail |
| 1 | Subway/Metro |
| 2 | Rail |
| 3 | Bus |
| 4 | Ferry |
| 700+ | Extended types |

**Sample:**
```
route_id,agency_id,route_short_name,route_long_name,route_desc,route_type,route_color,route_text_color,exact_times
"1-11B-M-sj2-1","700","11BM","Springwood, then all stations to Lithgow","Temporary buses","714","00B5EF","FFFFFF","1"
```

---

### trips.txt
**Individual trips/journeys on a route**

| Column | Description | Example |
|--------|-------------|---------|
| `route_id` | Which route | `1-11B-M-sj2-1` |
| `service_id` | Which calendar service | `AA55+1` |
| `trip_id` | Unique trip identifier | `1.AA55.1-11B-M-sj2-1.2.R` |
| `shape_id` | GPS path reference | `1-11B-M-sj2-1.2.R` |
| `trip_headsign` | Destination sign | `Springwood` |
| `direction_id` | 0=outbound, 1=inbound | `1` |
| `block_id` | Vehicle block | `` |
| `wheelchair_accessible` | 0=unknown, 1=yes, 2=no | `2` |
| `route_direction` | Direction description | `Lithgow, then all stations to Springwood` |
| `trip_note` | Special notes | `` |
| `bikes_allowed` | Bikes permitted | `` |

**Sample:**
```
route_id,service_id,trip_id,shape_id,trip_headsign,direction_id,block_id,wheelchair_accessible,route_direction,trip_note,bikes_allowed
"1-11B-M-sj2-1","AA55+1","1.AA55.1-11B-M-sj2-1.2.R","1-11B-M-sj2-1.2.R","Springwood","1","","2","Lithgow, then all stations to Springwood","",""
```

---

### stop_times.txt
**Arrival and departure times for each stop on each trip**

⚠️ **Large file (50MB+)** - Contains millions of rows

| Column | Description | Example |
|--------|-------------|---------|
| `trip_id` | Which trip | `1.AA51.1-SC0-1-sj2-1.1.R` |
| `arrival_time` | Arrival time (HH:MM:SS) | `22:50:00` |
| `departure_time` | Departure time | `22:50:00` |
| `stop_id` | Stop reference | `254111` |
| `stop_sequence` | Order of stops (1, 2, 3...) | `1` |
| `stop_headsign` | Headsign at this stop | `` |
| `pickup_type` | 0=regular, 1=no pickup | `0` |
| `drop_off_type` | 0=regular, 1=no drop off | `0` |
| `shape_dist_traveled` | Distance along shape (meters) | `16209.06` |
| `timepoint` | 1=exact time, 0=approximate | `1` |
| `stop_note` | Note reference | `` |

**Sample:**
```
trip_id,arrival_time,departure_time,stop_id,stop_sequence,stop_headsign,pickup_type,drop_off_type,shape_dist_traveled,timepoint,stop_note
"1.AA51.1-SC0-1-sj2-1.1.R","22:50:00","22:50:00","254111","1","","0","0","0.00","1",""
"1.AA51.1-SC0-1-sj2-1.1.R","23:04:00","23:04:00","253572","2","","0","0","16209.06","1",""
```

---

### calendar.txt
**Regular weekly service patterns**

| Column | Description | Example |
|--------|-------------|---------|
| `service_id` | Service identifier | `AA51+1` |
| `monday` | Runs Monday (1=yes, 0=no) | `1` |
| `tuesday` | Runs Tuesday | `1` |
| `wednesday` | Runs Wednesday | `1` |
| `thursday` | Runs Thursday | `1` |
| `friday` | Runs Friday | `1` |
| `saturday` | Runs Saturday | `0` |
| `sunday` | Runs Sunday | `0` |
| `start_date` | Service start (YYYYMMDD) | `20260311` |
| `end_date` | Service end | `20260609` |

**Sample:**
```
service_id,monday,tuesday,wednesday,thursday,friday,saturday,sunday,start_date,end_date
"AA51+1","1","1","1","1","1","0","0","20260311","20260609"
```

---

### calendar_dates.txt
**Service exceptions (holidays, special events)**

| Column | Description | Example |
|--------|-------------|---------|
| `service_id` | Service identifier | `AA51+1` |
| `date` | Exception date (YYYYMMDD) | `20260403` |
| `exception_type` | 1=added, 2=removed | `2` |

**Sample:**
```
service_id,date,exception_type
"AA51+1","20260403","2"  # Service removed on this date (likely a holiday)
```

---

### shapes.txt
**GPS coordinates defining route paths on a map**

⚠️ **Large file (50MB+)** - Contains millions of coordinate points

| Column | Description | Example |
|--------|-------------|---------|
| `shape_id` | Shape identifier | `1-11B-M-sj2-1.1.H` |
| `shape_pt_lat` | Latitude | `-33.69890300` |
| `shape_pt_lon` | Longitude | `150.56349931` |
| `shape_pt_sequence` | Point order (1, 2, 3...) | `1` |
| `shape_dist_traveled` | Distance from start (meters) | `0.00` |

**Sample:**
```
shape_id,shape_pt_lat,shape_pt_lon,shape_pt_sequence,shape_dist_traveled
"1-11B-M-sj2-1.1.H","-33.69890300","150.56349931","1","0.00"
"1-11B-M-sj2-1.1.H","-33.69886741","150.56350829","2","4.04"
```

---

### notes.txt
**Special notes referenced by trips**

| Column | Description | Example |
|--------|-------------|---------|
| `note_id` | Note identifier | `tw1` |
| `note_text` | Full note text | `This service departs after midnight...` |

**Sample:**
```
note_id,note_text
"tw1","This service departs after midnight / early the following day"
"VA","Free service is operated using a historic double deck bus..."
```

---

### levels.txt
**Station levels (for multi-level stations)**

| Column | Description | Example |
|--------|-------------|---------|
| `level_id` | Level identifier | `Level 1` |
| `level_index` | Numeric index | `1` |
| `level_name` | Display name | `` |

**Sample:**
```
level_id,level_index,level_name
"Level 0","0",""
"Level -1","-1",""
"Level 1","1",""
```

---

### pathways.txt
**Walking paths within stations (stairs, elevators, etc.)**

| Column | Description | Example |
|--------|-------------|---------|
| `pathway_id` | Pathway identifier | `2777191_277720_DP2_stairs_1` |
| `from_stop_id` | Starting stop/platform | `2777191` |
| `to_stop_id` | Ending stop/platform | `277720_DP2` |
| `pathway_mode` | Type (see below) | `2` |
| `is_bidirectional` | 1=both ways | `1` |
| `traversal_time` | Walking time (seconds) | `30` |

**Pathway Modes:**
| Code | Type |
|------|------|
| 1 | Walkway |
| 2 | Stairs |
| 3 | Moving sidewalk |
| 4 | Escalator |
| 5 | Elevator |
| 6 | Fare gate |
| 7 | Exit gate |

**Sample:**
```
pathway_id,from_stop_id,to_stop_id,pathway_mode,is_bidirectional,traversal_time
"2777191_277720_DP2_stairs_1","2777191","277720_DP2","2","1","30"
"2777191_277720_DP2_elevator_1","2777191","277720_DP2","5","1","60"
```

---

## 🔗 How Files Connect

```
agency.txt ──┐
             │
routes.txt ──┼── route_id ──► trips.txt ──┬── trip_id ──► stop_times.txt
             │                            │
             │                            └── shape_id ──► shapes.txt
             │
             └── service_id ──► calendar.txt
                              ──► calendar_dates.txt

stops.txt ◄── stop_id ── stop_times.txt
          ◄── from/to_stop_id ── pathways.txt

levels.txt ◄── level_id ── stops.txt

notes.txt ◄── trip_note/stop_note ── trips.txt/stop_times.txt
```

---

## 📚 Further Reading

- [GTFS Official Specification](https://gtfs.org/schedule/reference/)
- [NSW Transport Open Data](https://opendata.transport.nsw.gov.au/)
