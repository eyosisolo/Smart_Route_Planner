# Smart Route Planner

A Flask-based delivery route planner that lets drivers set their starting location, add customer addresses, select specific deliveries, and calculate an optimized route on an interactive map.

## Features

- Add customer locations using addresses
- Set the driver's starting location
- Select specific customers for a route
- Delete saved locations
- Display locations on an interactive map
- Calculate optimized delivery routes
- Show delivery order, route distance, and estimated travel time at 30 mph

## Technologies

Python · Flask · SQLite · HTML · CSS · JavaScript · OpenStreetMap · Nominatim · Leaflet · OSRM

## How It Works

```text
Address
   ↓
Nominatim
   ↓
Coordinates
   ↓
SQLite
   ↓
Selected Locations
   ↓
OSRM
   ↓
Route on Map
```

## Run

```bash
pip install -r requirements.txt
python app.py
```

Open:
http://127.0.0.1:5000
