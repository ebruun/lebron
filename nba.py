from datetime import datetime, timedelta

import requests
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2


kareem_player_id = "76003"
lebron_player_id = "2544"

cache_refresh_seconds = 5
_cache = {}

local_proxy = "http://2f32d1f76740.ngrok.io/update_points"


def get_player_total_pts(id_num):
    career = PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season
    total_pts = totals_reg.get_data_frame()["PTS"][0]

    return total_pts


def fetch_lebron_points_countdown():
    """On the road to become number 1, only Kareem to pass!"""
    lebron_total_points = get_player_total_pts(id_num=lebron_player_id)
    kareem_total_points = get_player_total_pts(id_num=kareem_player_id)

    return str(max(0, kareem_total_points - lebron_total_points))


def fetch_lebron_points_countdown_local():
    return requests.get(local_proxy).text


def lebron_points_countdown():
    cache_invalidation_time = datetime.now() - timedelta(seconds=cache_refresh_seconds)

    if _cache.get("timestamp", datetime.min) < cache_invalidation_time:
        _cache.update(
            {"timestamp": datetime.now(), "points": fetch_lebron_points_countdown()}
        )

    return _cache["points"]
