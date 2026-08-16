import requests


NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"


def geocode_address(address):

    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "SmartRoutePlanner/1.0"
    }

    try:

        response = requests.get(
            NOMINATIM_URL,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        results = response.json()

        if not results:

            return None

        latitude = float(results[0]["lat"])
        longitude = float(results[0]["lon"])

        return latitude, longitude

    except requests.RequestException:

        return None