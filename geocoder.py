import requests


def geocode_address(address):

    url = "https://nominatim.openstreetmap.org/search"

    parameters = {
        "q": address,
        "format": "jsonv2",
        "limit": 1
    }

    headers = {
        "User-Agent": "SmartRoutePlanner/1.0"
    }

    response = requests.get(
        url,
        params=parameters,
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        return None

    results = response.json()

    if not results:
        return None

    location = results[0]

    return {
        "latitude": float(location["lat"]),
        "longitude": float(location["lon"])
    }