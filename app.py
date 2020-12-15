from flask import Flask, render_template, request, json

from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

app = Flask(__name__)

def get_player_total_pts(id_num):
    p = players.find_player_by_id(id_num)

    career = playercareerstats.PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season

    total_pts = totals_reg.get_data_frame()["PTS"][0]

    #print(career.get_data_frames()[0])
    #print(a.get_data_frame())
    #print(a.get_data_frame()["PTS"])

    #print('{} has {} points'.format(p['full_name'], total_pts))
    return total_pts

@app.route('/')
def start_page():
    return render_template('main_page.html', value1 = str(0), value2 = str(0))

@app.route("/", methods=['POST'])
def reload_data():
    a = get_player_total_pts(2544)
    b = get_player_total_pts(76003)
    return render_template('main_page.html', value1 = str(b), value2 = str(a))

if __name__=="__main__":
    app.run()