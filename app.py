import json

from flask import Flask
from nba_api.stats.endpoints import playercareerstats

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_point_countdown():
    lebron_career_obj = playercareerstats.PlayerCareerStats(player_id="2544")
    # lebron_totals_dict = lebron_career_obj.career_totals_regular_season.get_dict()
    lebron_total_points = int(lebron_career_obj.career_totals_regular_season.get_data_frame()["PTS"][0])
    return json.dumps({
        "current_total_points": lebron_total_points,
    })

if __name__ == '__main__':
    app.run()