import math

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the approximate distance between two geeographic coodinates."""

    earth_radius = 6371  # in kilometers

    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)

    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    difference_latitude = lat2 - lat1
    difference_longitude = lon2 - lon1

    a = (math.sin(difference_latitude / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(difference_longitude / 2) ** 2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = earth_radius * c
    return distance

