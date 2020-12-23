from flask import Flask, Response, render_template

from nba import fetch_lebron_points_countdown_local


app = Flask(__name__)


@app.route("/")
def start_page():
    point_diff = fetch_lebron_points_countdown_local()

    return render_template("main_page.html", value=str(point_diff))


@app.route("/update_points")
def update_points():
    def generate():
        return fetch_lebron_points_countdown_local()

    return Response(generate(), mimetype="text")


if __name__ == "__main__":
    app.run()
