from flask import Flask, request, send_from_directory
from flask.templating import render_template
from map_creator.main_code import get_lat_long, all_average_efficiency, create_txt, map_generator

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("mainpage.html")


@app.route("/about_us.html")
def about():
    return render_template("about_us.html")


@app.route("/contact_us.html")
def contact():
    return render_template("contact_us.html")


@app.route("/solar_panels.html")
def panels():
    return render_template("solar_panels.html")


@app.route("/wind_turbines.html")
def turbines():
    return render_template("wind_turbines.html")


# @app.route("/map")
# def map():
#     return render_template()


@app.route("/redirect.html", methods=["GET", "POST"])
def redirect():
    latitude = float(request.form.get("latitude"))
    longtitude = float(request.form.get("longtitude"))
    distance = float(request.form.get("distance"))
    energy_type = request.form.get("type")  # "solar" or "wind"

    if request.method == "POST":
        locations = get_lat_long(latitude, longtitude, distance)
        eff = all_average_efficiency(locations, energy_type, "forecast")
        map_generator(eff[0], (latitude, longtitude), eff[1])

        create_txt(eff, energy_type, "files/results.txt")

        if request.form.get("action") == "OPEN MAP":
            return render_template("map.html")
        elif request.form.get("action") == "DOWNLOAD RESULTS":
            return send_from_directory("files", "results.txt", as_attachment=True)

    return render_template("mainpage.html")


if __name__ == "__main__":
    app.run(debug=True)
