from route_engine import calculate_distance


locations = {
    "Start": (9.0300, 38.7400),
    "Customer A": (9.0400, 38.7500),
    "Customer B": (9.0500, 38.7600),
    "Customer C": (9.0200, 38.7300),
    "Customer D": (9.0600, 38.7300)
}


start = locations["Start"]


for name, coordinates in locations.items():

    if name == "Start":
        continue

    distance = calculate_distance(
        start[0],
        start[1],
        coordinates[0],
        coordinates[1]
    )

    print(name, ":", round(distance, 2), "km")