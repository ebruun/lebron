from flask import Flask, render_template, url_for, Response

from datetime import datetime
import time

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

app = Flask(__name__)


def get_player_total_pts(id_num):

    career = playercareerstats.PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season

    total_pts = totals_reg.get_data_frame()["PTS"][0]

    p = players.find_player_by_id(id_num)
    print("{} has {} points".format(p["full_name"], total_pts))
    return total_pts


@app.route("/")
def start_page():
    #b = get_player_total_pts(76003)
    #a = get_player_total_pts(2544)
    b = 0
    a = 0
    
    diff = b - a
    return render_template("main_page.html", value1=str(0), value2=str(0), value3=str(diff))

""" 
@app.route("/", methods=["POST"])
def reload_page():
    #b = get_player_total_pts(76003)
    #a = get_player_total_pts(2544)
    b = 0
    a = 0
    
    diff = b - a
    return render_template(
        "main_page.html", value1=str(b), value2=str(a), value3=str(diff)
    ) """

""" @app.route('/time_feed')
def time_feed():

    def generate():
        
        yield datetime.now().strftime("%Y.%m.%d|%H:%M:%S")  # return also will work

    return Response(generate(), mimetype='text') """

@app.route('/update_points')
def update_points():
    def generate2():
        
        b = get_player_total_pts(76003)
        a = get_player_total_pts(2544)
    
        diff = b - a
        yield str(diff)  # return also will work

    return Response(generate2(), mimetype='text')


if __name__ == "__main__":
    app.run(debug=True)