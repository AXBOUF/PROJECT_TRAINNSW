# Sydney Trains Real-Time Tracker (WIP)

> A personal project to build a real-time train tracking app using Transport for NSW data — designed to explore full stack development, cloud architecture, and data engineering in a practical and personal context.

---

## What This Is

This project pulls **real-time train data** from the [Transport for NSW API](https://opendata.transport.nsw.gov.au/) and displays key info for **personalized routes** like:

- Central → Parramatta
- Home → Uni
- (More to come)

It’s a **lightweight, custom-built dashboard**, not a full-feature trip planner.

---

## Why I'm Building This

- To learn full stack development hands-on (Python, React, AWS)
- To experiment with real-time APIs and microservices
- To build something I’ll actually use day-to-day
- To create a **portfolio-ready project** grounded in real-world data

---

## ⚙️ Project Scope

| Layer         | What It Does                                     |
|---------------|--------------------------------------------------|
| Backend     | Fetches and parses GTFS Realtime feeds          |
| Frontend    | Displays filtered routes & next train info      |
| Cloud       | AWS hosting, caching, microservices (later)     |
| Personalization | Set favorite routes, view live status            |
| Voice UI    | (Optional) Ask: "When’s the next train to X?"   |

---

## Rough Architecture

- Gotta register for the open data api( it is free for personal purpose )
- After then we will try some solution architect best practices to continue

