import requests


OSRM_URL = "https://router.project-osrm.org/trip/v1/driving"


# Starting point for the delivery route.
START_LATITUDE = 9.0300
START_LONGITUDE = 38.7400


def calculate_route(locations):

    if not locations:
        return None

    # The first point is always our starting point.
    coordinates = [
        (
            START_LONGITUDE,
            START_LATITUDE
        )
    ]

    # Add all customers.
    for location in locations:

        coordinates.append(
            (
                float(location["longitude"]),
                float(location["latitude"])
            )
        )

    # OSRM expects:
    # longitude,latitude
    coordinate_string = ";".join(
        f"{longitude},{latitude}"
        for longitude, latitude in coordinates
    )

    url = f"{OSRM_URL}/{coordinate_string}"

    params = {
        "overview": "full",
        "geometries": "geojson",
        "steps": "true",
        "source": "first",
        "roundtrip": "false"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:

        print("Routing request failed:", error)

        return None

    if data.get("code") != "Ok":

        print("OSRM returned an unsuccessful response.")

        return None

    trips = data.get("trips")

    if not trips:

        return None

    trip = trips[0]

    # OSRM returns waypoint information showing
    # the optimized order.
    waypoints = data.get("waypoints", [])

    ordered_locations = []

    for waypoint in sorted(
        waypoints,
        key=lambda item: item["waypoint_index"]
    ):

        input_index = waypoint.get(
            "waypoint_index"
        )

        # The first input point is our starting point.
        if input_index == 0:
            continue

        location_index = input_index - 1

        if 0 <= location_index < len(locations):

            location = locations[location_index]

            ordered_locations.append({
                "id": location["id"],
                "name": location["name"],
                "address": location["address"],
                "latitude": location["latitude"],
                "longitude": location["longitude"]
            })

    return {
        "distance": trip["distance"],
        "duration": trip["duration"],
        "geometry": trip["geometry"],
        "ordered_locations": ordered_locations
    }