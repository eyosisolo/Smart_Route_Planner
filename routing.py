import requests


OSRM_URL = (
    "https://router.project-osrm.org/"
    "trip/v1/driving"
)


AVERAGE_SPEED_MPH = 30


def calculate_route(
    driver_start,
    locations
):

    if driver_start is None:
        return None

    if len(locations) < 2:
        return None

    # Start from the driver's actual location.
    coordinates = [
        (
            float(driver_start["longitude"]),
            float(driver_start["latitude"])
        )
    ]

    # Add selected customers.
    for location in locations:

        coordinates.append(
            (
                float(location["longitude"]),
                float(location["latitude"])
            )
        )

    # OSRM uses:
    # longitude,latitude
    coordinate_string = ";".join(
        f"{longitude},{latitude}"
        for longitude, latitude in coordinates
    )

    url = (
        f"{OSRM_URL}/"
        f"{coordinate_string}"
    )

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

        print(
            "Routing request failed:",
            error
        )

        return None

    if data.get("code") != "Ok":

        print(
            "OSRM returned an unsuccessful response."
        )

        return None

    trips = data.get("trips")

    if not trips:
        return None

    trip = trips[0]

    # OSRM gives distance in meters.
    distance_meters = trip["distance"]

    # Convert meters to miles.
    distance_miles = (
        distance_meters / 1609.344
    )

    # Calculate time using 30 mph.
    travel_time_hours = (
        distance_miles / AVERAGE_SPEED_MPH
    )

    travel_time_minutes = (
        travel_time_hours * 60
    )

    # Get the optimized waypoint order.
    waypoints = data.get(
        "waypoints",
        []
    )

    ordered_locations = []

    sorted_waypoints = sorted(
        waypoints,
        key=lambda item: item["waypoint_index"]
    )

    for waypoint in sorted_waypoints:

        waypoint_index = waypoint.get(
            "waypoint_index"
        )

        # The first point is the driver start.
        if waypoint_index == 0:
            continue

        location_index = (
            waypoint_index - 1
        )

        if (
            0 <= location_index
            < len(locations)
        ):

            location = locations[
                location_index
            ]

            ordered_locations.append({

                "id":
                    location["id"],

                "name":
                    location["name"],

                "address":
                    location["address"],

                "latitude":
                    location["latitude"],

                "longitude":
                    location["longitude"]
            })

    return {

        "distance":
            distance_meters,

        "distance_miles":
            distance_miles,

        "duration":
            travel_time_minutes,

        "average_speed_mph":
            AVERAGE_SPEED_MPH,

        "geometry":
            trip["geometry"],

        "ordered_locations":
            ordered_locations
    }