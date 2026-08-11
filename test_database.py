from location_repository import (
    create_locations_table,
    add_location,
    get_all_locations
)


create_locations_table()

add_location("Start", 9.0300, 38.7400)
add_location("Customer A", 9.0400, 38.7500)
add_location("Customer B", 9.0500, 38.7600)
add_location("Customer C", 9.0200, 38.7300)


locations = get_all_locations()


for location in locations:

    print(
        location["id"],
        location["name"],
        location["latitude"],
        location["longitude"]
    )