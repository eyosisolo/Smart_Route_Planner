from flask import Flask, render_template, request, redirect, url_for

from location_repository import (
    create_locations_table,
    add_location,
    get_all_locations
)

from geocoder import geocode_address

from routing import calculate_route


app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)


# Create the database table when the application starts.
create_locations_table()


@app.route("/")
def home():

    # get_all_locations() now returns
    # normal dictionaries, not sqlite3.Row objects.
    locations = get_all_locations()

    return render_template(
        "index.html",
        locations=locations,
        route=None,
        message=None
    )


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
            error="Customer name and address are required."
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


@app.route("/route")
def route():

    locations = get_all_locations()

    if len(locations) == 0:

        return render_template(
            "index.html",
            locations=locations,
            route=None,
            message="Add at least one location first."
        )

    route_data = calculate_route(locations)

    if route_data is None:

        return render_template(
            "index.html",
            locations=locations,
            route=None,
            message=(
                "The route could not be calculated. "
                "Please make sure you have valid locations."
            )
        )

    return render_template(
        "index.html",
        locations=locations,
        route=route_data,
        message=None
    )


if __name__ == "__main__":

    app.run(debug=True)