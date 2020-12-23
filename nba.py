from datetime import datetime, timedelta, date

import requests
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats

from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog
from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2

from nba_api.stats.endpoints.playernextngames import PlayerNextNGames

kareem_player_id = "76003"
#lebron_player_id = "2544"
lebron_player_id = '203507' #Giannis

cache_refresh_seconds = 5
_cache = {}

local_proxy = "http://2f32d1f76740.ngrok.io/update_points"


def check_if_game_today():

    today = date.today()
    diff = timedelta(0)
    today = (today- diff).strftime('%b %d, %Y').upper()

    df = PlayerNextNGames(player_id = lebron_player_id, number_of_games=5).next_n_games.get_data_frame()

    df_today = df.loc[(df['GAME_DATE'] == today)]

    print(df_today)

    if df_today.empty:
        print("No Game Today")

        #just for testing
        #game_ID = '0022000002' 
        #game_TIME = None
        game_ID = False
        game_TIME = False
    else:
        print("There is a Game Today")
        game_ID = df_today['GAME_ID'].values[0]
        game_TIME = df_today['GAME_TIME'].values[0]    
        
    return (game_ID, game_TIME)


def get_player_total_pts(id_num):
    career = PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season
    total_pts = totals_reg.get_data_frame()["PTS"][0]

    return total_pts


def fetch_lebron_points_countdown():
    """On the road to become number 1, only Kareem to pass!"""
    print("yoo")
    if check_if_game_today()[0]:
        pass
    else:
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
