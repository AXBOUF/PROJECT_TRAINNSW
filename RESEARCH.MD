# Research Notes: Real-World Transit Data Engineering Systems

## Introduction

These notes document real-world systems and architecture patterns for processing GTFS and GTFS-Realtime transit data feeds. They are intended to inform the design of a capstone Data Engineering project using Transport for NSW (TfNSW) open data. Studying these systems before building helps avoid common pitfalls and adopt proven patterns used in production transit platforms.

---

## 1. OneBusAway

OneBusAway is one of the most widely used open-source transit data systems. It powers public transit apps across multiple cities and is commonly referenced in academic and engineering contexts.

### What It Does

- Consumes GTFS static timetable data
- Consumes GTFS-Realtime feeds
- Merges schedule data with live vehicle positions
- Provides APIs for downstream transit applications
- Visualises vehicles on a map in real time

### Key Component: `onebusaway-gtfs-realtime-visualizer`

This component specifically demonstrates:

- Decoding GTFS-Realtime protocol buffer feeds
- Extracting vehicle positions from binary data
- Rendering vehicles on a live map interface

### Why It Is Useful to Study

- Shows how real-time transit feeds are decoded from protocol buffer format
- Demonstrates how vehicles are matched to scheduled trips
- Explains the merge strategy between static schedule data and live vehicle data

---

## 2. GTFS Data Pipeline for TfNSW Bus Data

This project processes Transport for NSW bus datasets directly — making it the most relevant reference for the capstone project.

### Pipeline Stages

1. Fetch GTFS-Realtime `.pb.gz` files from the TfNSW API
2. Decode protocol buffer format into structured records
3. Transform into tabular datasets
4. Aggregate by agency and time window
5. Produce cleaned analytics-ready datasets

### Architecture

```
GTFS-Realtime protobuf (.pb.gz)
        ↓
   decode (gtfs-realtime-bindings)
        ↓
   structured tables (Pandas / SQL)
        ↓
   analytics dataset (PostgreSQL / S3)
```

### Why It Is Useful

- Demonstrates the first and hardest step of any GTFS pipeline
- Shows how binary protobuf real-time feeds become structured, queryable datasets
- Uses the exact same TfNSW data ecosystem as the capstone project

---

## 3. hafas-gtfs-rt-feed

This project demonstrates a streaming microservices architecture commonly used in production transit data systems.

### Architecture Pattern

```
monitor-hafas (data collector)
        ↓
match-with-gtfs (matching engine)
        ↓
serve-as-gtfs-rt (API layer)
```

Services communicate through streaming channels, demonstrating a loosely coupled, event-driven design.

### Generalised Pattern

```
collector service
        ↓
message queue (Kafka / Kinesis)
        ↓
matching service (trip ↔ vehicle)
        ↓
API / serving layer
```

This pattern is common in many real-time transit platforms at scale. Understanding it helps when designing a modular pipeline that can be extended later.

---

## 4. TransitGPT

TransitGPT is a research project combining GTFS structured transit data with large language models (LLMs). This is directly relevant to the GenAI requirement of the capstone project.

### How It Works

**Example interaction:**

> User: "Which routes stop at Central Station?"

**System flow:**

1. LLM receives the natural language question
2. LLM generates Python code to query the GTFS dataset
3. Code is executed against the structured data
4. Result is returned to the user as a natural language answer

### Architecture

```
User Question (natural language)
        ↓
LLM (generates Python / SQL query)
        ↓
Query GTFS dataset (PostgreSQL / Parquet)
        ↓
Execute query
        ↓
Return analysis to user
```

### Why It Is Useful

- Demonstrates a justified, architectural use of LLMs — not just a chatbot
- Shows how AI can query structured transit datasets programmatically
- Maps directly to the "AI Agent with tool calling" pattern used in the capstone design

---

## 5. CityPulse

CityPulse is a research platform for large-scale urban mobility data processing. It represents a production-scale reference architecture.

### Architecture

```
Kafka (streaming ingestion)
        ↓
Spark Streaming (real-time processing)
        ↓
Data Warehouse (historical storage)
        ↓
ML prediction (delay forecasting)
        ↓
Dashboard (visualisation layer)
```

### Why It Is Useful

- Shows the full stack of a mature mobility data platform
- Demonstrates where ML and prediction fit in the pipeline
- Useful reference when designing the analytics and forecasting layers of the capstone

---

## Key Architecture Pattern in Transit Data Systems

Most real-world transit data platforms — regardless of scale — follow the same core pattern:

```
┌─────────────────────────────────┐
│  GTFS Static (schedule files)   │
│  +                              │
│  GTFS-Realtime (live vehicles)  │
└─────────────────────────────────┘
                ↓
        ┌───────────────┐
        │   Ingestion   │
        └───────────────┘
                ↓
        ┌───────────────────────────┐
        │      Matching Engine      │
        │   (trip ↔ vehicle ID)     │
        └───────────────────────────┘
                ↓
        ┌───────────────┐
        │   Data Store  │
        │ (PostgreSQL / │
        │  S3 / DWH)    │
        └───────────────┘
                ↓
  ┌─────────────────────────────┐
  │  Analytics / APIs / Apps    │
  │  (Dashboard, Agent, API)    │
  └─────────────────────────────┘
```

Understanding this pattern is the foundation for building any transit analytics system.

---

## Example Commuter Application Platform (Conceptual)

Transit platforms like **AnyTrip** (Sydney, founded 2017 by Ken Tsang) likely follow an architecture similar to this:

```
TfNSW Transit Feeds (GTFS + GTFS-R)
        ↓
Collector Service (polling / streaming)
        ↓
Matching Engine (trip ↔ vehicle ↔ route)
        ↓
Database (PostgreSQL / TimescaleDB)
        ↓
Map / API Layer (REST / WebSocket)
        ↓
Mobile or Web Application (user-facing)
```

A capstone project builds a simplified, solo version of this — with an AI Agent layer added on top for GenAI differentiation.

---

## Learning Strategy Before Building

### Step 1 — Study Reference Projects

- Read the OneBusAway `gtfs-realtime-visualizer` source code
- Study the TfNSW GTFS pipeline examples
- Review TransitGPT for the LLM + structured data pattern

### Step 2 — Run a Minimal Experiment First

Before building the full pipeline, write a minimal script:

```python
# Minimal GTFS-R experiment
import requests
from google.transit import gtfs_realtime_pb2

API_KEY = "your_key_here"
URL = "https://api.transport.nsw.gov.au/v1/gtfs/vehiclepos/buses"

response = requests.get(URL, headers={"Authorization": f"apikey {API_KEY}"})

feed = gtfs_realtime_pb2.FeedMessage()
feed.ParseFromString(response.content)

for entity in feed.entity:
    if entity.HasField("vehicle"):
        v = entity.vehicle
        print(v.trip.trip_id, v.position.latitude, v.position.longitude)
```

This single script removes most of the complexity of understanding GTFS-Realtime feeds. Do this before designing any infrastructure.

### Step 3 — Design Before Building

- Draw the pipeline architecture on paper or whiteboard
- Identify where static data ends and real-time data begins
- Identify where the AI agent layer plugs in
- Then write code

---

## Important Insight

> The hardest problem in transit data systems is **not** retrieving the data.
> The real challenge is **matching real-time vehicle information with scheduled trip data.**

### The Core Relationship Chain

```
vehicle_id  →  trip_id  →  route_id  →  stop_id
```

This chain must be resolved correctly before any analytics, predictions, or AI agent queries will produce accurate results.

Once this relationship is solved:
- On-time performance calculation becomes straightforward
- Delay aggregation by route and time window is simple
- AI agent queries over the data produce reliable answers
- Dashboard visualisations are accurate

**Solving the matching problem is the engineering core of the capstone project.**

---

## Quick Reference: TfNSW API Details

| Item | Detail |
|---|---|
| Base URL | `https://api.transport.nsw.gov.au` |
| Auth header | `Authorization: apikey YOUR_KEY` |
| Default plan | Bronze — 60,000 calls/day, 5/sec |
| GTFS format docs | https://developers.google.com/transit/gtfs/reference |
| GTFS-R format docs | https://developers.google.com/transit/gtfs-realtime/reference |
| Buses real-time update | Every 10 seconds |
| Sydney Trains real-time | Every 10 seconds |
| Ferries real-time | Every 30 seconds |
| NSW Trains real-time | Every 30 seconds |
| GTFS static update | Nightly (varies by mode) |

---

*Notes compiled for capstone project research — Data Engineering, Sydney, Australia.*
