from flask import Flask, Response, render_template

#from nba import fetch_lebron_points_countdown_local as fetch_points
from nba import lebron_points_countdown as fetch_points

app = Flask(__name__)


@app.route("/")
def start_page():
    point_diff = fetch_points()

    return render_template("main_page.html", value=str(point_diff))


@app.route("/update_points")
def update_points():
    def generate():
        return fetch_points()

    return Response(generate(), mimetype="text")


if __name__ == "__main__":
    app.run(debug=True)
