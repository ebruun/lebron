from datetime import datetime, timedelta

from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.static import players


kareem_player_id = "76003"
lebron_player_id = "2544"

cache_refresh_seconds = 5

_cache = {}


def get_player_total_pts(id_num):
    career = PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season
    total_pts = totals_reg.get_data_frame()["PTS"][0]

    return total_pts


def fetch_lebron_points_countdown():
    """On the road to become number 1, only Kareem to pass!"""
    # lebron_total_points = get_player_total_pts(id_num=lebron_player_id)
    # kareem_total_points = get_player_total_pts(id_num=kareem_player_id)

    lebron_total_points = players.find_players_by_first_name("lebron")[0]["id"]
    kareem_total_points = players.find_players_by_first_name("kareem")[0]["id"]

    return str(max(0, kareem_total_points - lebron_total_points))


def lebron_points_countdown():
    cache_invalidation_time = datetime.now() - timedelta(seconds=cache_refresh_seconds)

    if _cache.get("timestamp", datetime.min) < cache_invalidation_time:
        _cache.update(
            {"timestamp": datetime.now(), "points": fetch_lebron_points_countdown()}
        )

    return _cache["points"]
