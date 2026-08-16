import requests


OSRM_URL = "https://router.project-osrm.org/trip/v1/driving"


# Starting point for the delivery route.
# Addis Ababa.
START_LATITUDE = 9.0300
START_LONGITUDE = 38.7400


def calculate_route(locations):

    if not locations:

        return None

    # Start from the delivery starting point.
    coordinates = [
        (
            START_LONGITUDE,
            START_LATITUDE
        )
    ]

    # Add every saved customer.
    for location in locations:

        coordinates.append(
            (
                float(location["longitude"]),
                float(location["latitude"])
            )
        )

    # Convert coordinates to OSRM format:
    #
    # longitude,latitude;longitude,latitude
    #
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

        if data.get("code") != "Ok":

            return None

        trips = data.get("trips")

        if not trips:

            return None

        trip = trips[0]

        return {
            "distance": trip["distance"],
            "duration": trip["duration"],
            "geometry": trip["geometry"]
        }

    except requests.RequestException:

        return None