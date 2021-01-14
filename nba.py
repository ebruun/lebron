from datetime import date, datetime, timedelta, timezone

import requests
from pytz import timezone


kareem_player_id = "76003"
kareem_static_points = 38387

lebron_player_id = "2544"

tip_off_buffer = 15  # game doesnt start right at listed time, assume this buffer
update_buffer = 30  # assume it takes 30 mins to update the static page

cache_refresh_seconds = 5
_cache = {}


def check_if_game_today():
    """ check if there is a game today, and live updating required """
    today = datetime.now(timezone("EST"))

    # based on .json format, set December to 0
    if today.month == 12:
        idx = 0
    else:
        idx = today.month

    # edge case, if the game goes into next day (2am) reset the date to start
    if today.hour < 2:
        today = today - timedelta(1)
        today.replace(hour=23, minute=59)

    get_url = "https://ca.global.nba.com/stats2/team/schedule.json?countryCode=CA&locale=en&teamCode=lakers"

    data = requests.get(get_url).json()
    data = data["payload"]["monthGroups"][idx]["games"]  # games in the month

    game_ID = None

    print("today is {}-{}, hour: {}".format(today.month, today.day, today.hour))
    for row in data:
        game_date = row["profile"]["dateTimeEt"]
        game_date = datetime.strptime(game_date, "%Y-%m-%dT%H:%M")

        game_status = row["boxscore"]["statusDesc"]

        if game_date.day == today.day:
            print("there is a game today")

            if game_status:
                print("game has started")
                game_ID = row["profile"]["gameId"]
                return game_ID, game_date
            else:
                print("game not started")
                return game_ID, game_date

    print("there is no game today")
    return None, None


def check_if_update_finished(game_date, duration):
    end_time = game_date + timedelta(minutes=duration + tip_off_buffer)

    end_time = end_time.replace(tzinfo=timezone("US/Eastern"))

    today = datetime.now(timezone("US/Eastern"))

    elapsed = (today - end_time).total_seconds() / 60

    print("end time", end_time, "today:", today)
    print("elapsed time since end:", elapsed)

    if elapsed > update_buffer:
        return True
    else:
        return False


def get_player_static_pts(player_ID):
    """ get the recorded total points scored by a player """
    get_url = "https://stats.nba.com/stats/leagueLeaders?ActiveFlag=No&LeagueID=00&PerMode=Totals&Scope=S&Season=All+Time&SeasonType=Regular+Season&StatCategory=PTS"
    data = requests.get(get_url).json()

    for row in data["resultSet"]["rowSet"]:
        if row[0] == int(player_ID):
            total_pts = row[21]
            break

    return total_pts


def get_player_live_pts(game_ID, player_ID):
    """ get the data from the URL for the game being played """
    get_url = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{}.json".format(
        game_ID
    )

    # boxscore status for some reason updates much faster than teamschedule .json
    try:
        print("Get points from: ", get_url)
        data = requests.get(get_url).json()
        status = data["game"]["gameStatusText"]
        duration = data["game"]["duration"]

        return json_extract(data, "personId", "points", player_ID), status, duration
    except:
        print("error getting points from: ", get_url)
        return 0, None, None


def json_extract(obj, key, key2, player_ID):
    """Recursively fetch values from nested JSON."""
    arr = []
    save_flag = False

    def extract(obj, arr, key, key2, save_flag):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key, key2, save_flag)

                # Find Player
                elif k == key and v == int(player_ID):
                    save_flag = True

                # Save Points
                elif k == key2 and save_flag:
                    arr.append(v)
                    save_flag = False

        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key, key2, save_flag)
        return arr

    values = extract(obj, arr, key, key2, save_flag)
    return values[0]


def fetch_lebron_points_countdown():
    """On the road to become number 1, only Kareem to pass!"""

    game_id, game_date = check_if_game_today()
    lebron_live_points = 0

    if game_id:
        lebron_live_points, game_status, duration = get_player_live_pts(
            game_ID=game_id, player_ID=lebron_player_id
        )
        print("Game Status: ", game_status)

        if game_status == "Final":
            if check_if_update_finished(game_date, duration):
                print("Game Finished: Enough time elapsed to have updated static")
                lebron_live_points = 0
            else:
                print("Game Finished: Still updating static")

    lebron_static_points = get_player_static_pts(player_ID=lebron_player_id)

    print(
        "static points = {}, live points = {}\n".format(
            lebron_static_points, lebron_live_points
        )
    )

    return str(
        max(0, kareem_static_points - (lebron_static_points + lebron_live_points))
    )


def lebron_points_countdown():
    """buffer, called from flask app"""
    cache_invalidation_time = datetime.now() - timedelta(seconds=cache_refresh_seconds)

    if _cache.get("timestamp", datetime.min) < cache_invalidation_time:
        _cache.update(
            {"timestamp": datetime.now(), "points": fetch_lebron_points_countdown()}
        )

    return _cache["points"]
