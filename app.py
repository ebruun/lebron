from flask import Flask, Response, render_template
from waitress import serve
from flask_cors import CORS

from nba import lebron_points_countdown



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/")
def start_page():
    point_diff = lebron_points_countdown()

    return render_template("main_page.html", value=str(point_diff))


@app.route("/update_points")
def update_points():
    def generate():
        return lebron_points_countdown()

    return Response(generate(), mimetype="text")


if __name__ == "__main__":
    #app.run()
    serve(app, port=8080)