from flask import Flask, Response, render_template

from nba import lebron_points_countdown


app = Flask(__name__)


@app.route("/")
def start_page():
    point_diff = lebron_points_countdown()
    return render_template(
        "main_page.html", value1=str(0), value2=str(0), value3=str(point_diff)
    )


@app.route("/update_points")
def update_points():
    def generate2():
        return lebron_points_countdown()

    return Response(generate2(), mimetype="text")


if __name__ == "__main__":
    app.run(debug=True)
