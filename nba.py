from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats


kareem_player_id = "76003"
lebron_player_id = "2544"


def get_player_total_pts(id_num):
    career = PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season
    total_pts = totals_reg.get_data_frame()["PTS"][0]

    return total_pts


def lebron_points_countdown():
    """On the road to become number 1, only Kareem to pass!"""
    lebron_total_points = get_player_total_pts(id_num=lebron_player_id)
    kareem_total_points = get_player_total_pts(id_num=kareem_player_id)

    return str(max(0, kareem_total_points - lebron_total_points))
