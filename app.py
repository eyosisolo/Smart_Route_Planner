from flask import Flask, render_template, request, redirect, url_for  

from location_repository import (
    create_locations_table,
    add_location,
    get_all_locations
)


app = Flask(__name__)


create_locations_table()


@app.route("/")
def home():

    locations = get_all_locations()

    return render_template(
        "index.html",
        locations=locations
    )


@app.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        name = request.form["name"]

        latitude = float(request.form["latitude"])

        longitude = float(request.form["longitude"])

        add_location(
            name,
            latitude,
            longitude
        )

        return redirect(url_for("home"))

    return render_template("add_location.html")


if __name__ == "__main__":
    app.run(debug=True)