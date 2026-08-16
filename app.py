from flask import Flask, render_template, request, redirect, url_for

from location_repository import (
    create_locations_table,
    create_driver_start_table,
    add_location,
    get_all_locations,
    get_locations_by_ids,
    delete_location,
    save_driver_start,
    get_driver_start
)

from geocoder import geocode_address

from routing import calculate_route


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)


# ============================================================
# DATABASE SETUP
# ============================================================

create_locations_table()
create_driver_start_table()


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    locations = get_all_locations()

    driver_start = get_driver_start()

    return render_template(
        "index.html",
        locations=locations,
        driver_start=driver_start,
        route=None,
        selected_ids=[],
        message=None
    )


# ============================================================
# ADD CUSTOMER LOCATION
# ============================================================

@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "GET":

        return render_template(
            "add_location.html",
            error=None
        )

    name = request.form.get(
        "name",
        ""
    ).strip()

    address = request.form.get(
        "address",
        ""
    ).strip()

    if not name or not address:

        return render_template(
            "add_location.html",
            error=(
                "Customer name and address "
                "are required."
            )
        )

    coordinates = geocode_address(address)

    if coordinates is None:

        return render_template(
            "add_location.html",
            error=(
                "Location could not be found. "
                "Please enter a more specific address."
            )
        )

    latitude, longitude = coordinates

    add_location(
        name,
        address,
        latitude,
        longitude
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# SET DRIVER START
# ============================================================

@app.route(
    "/driver-start",
    methods=["POST"]
)
def set_driver_start():

    address = request.form.get(
        "driver_start_address",
        ""
    ).strip()

    if not address:

        return redirect(
            url_for("home")
        )

    coordinates = geocode_address(address)

    if coordinates is None:

        locations = get_all_locations()

        driver_start = get_driver_start()

        return render_template(
            "index.html",
            locations=locations,
            driver_start=driver_start,
            route=None,
            selected_ids=[],
            message=(
                "Driver starting location could not "
                "be found. Please enter a more "
                "specific address."
            )
        )

    latitude, longitude = coordinates

    save_driver_start(
        address,
        latitude,
        longitude
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# CALCULATE ROUTE
# ============================================================

@app.route(
    "/route",
    methods=["POST"]
)
def route():

    selected_ids = request.form.getlist(
        "location_ids"
    )

    selected_ids = [
        int(location_id)
        for location_id in selected_ids
    ]

    locations = get_all_locations()

    driver_start = get_driver_start()

    # Driver start is required.
    if driver_start is None:

        return render_template(
            "index.html",
            locations=locations,
            driver_start=None,
            route=None,
            selected_ids=selected_ids,
            message=(
                "Please set the driver's starting "
                "location first."
            )
        )

    # At least two delivery locations are required.
    if len(selected_ids) < 2:

        return render_template(
            "index.html",
            locations=locations,
            driver_start=driver_start,
            route=None,
            selected_ids=selected_ids,
            message=(
                "Please select at least two "
                "delivery locations."
            )
        )

    selected_locations = get_locations_by_ids(
        selected_ids
    )

    if len(selected_locations) < 2:

        return render_template(
            "index.html",
            locations=locations,
            driver_start=driver_start,
            route=None,
            selected_ids=selected_ids,
            message=(
                "The selected locations could "
                "not be found."
            )
        )

    route_data = calculate_route(
        driver_start,
        selected_locations
    )

    if route_data is None:

        return render_template(
            "index.html",
            locations=locations,
            driver_start=driver_start,
            route=None,
            selected_ids=selected_ids,
            message=(
                "The route could not be calculated. "
                "Please try again."
            )
        )

    return render_template(
        "index.html",
        locations=locations,
        driver_start=driver_start,
        route=route_data,
        selected_ids=selected_ids,
        message=None
    )


# ============================================================
# DELETE CUSTOMER LOCATION
# ============================================================

@app.route(
    "/delete/<int:location_id>",
    methods=["POST"]
)
def delete(location_id):

    delete_location(location_id)

    return redirect(
        url_for("home")
    )


# ============================================================
# RUN APPLICATION
# ============================================================

if __name__ == "__main__":

    app.run(debug=True)