from datetime import datetime, timedelta, date
import requests

#from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
#from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog
#from nba_api.stats.static import players
#from nba_api.stats.endpoints.playernextngames import PlayerNextNGames

kareem_player_id = "76003"
kareem_static_points = 38387

lebron_player_id = "2544"
#lebron_player_id = '201566' #Westbrook (playing today)
#lebron_player_id = '203507' #Giannis (playing today)

cache_refresh_seconds = 5
_cache = {}

local_proxy = "http://2f32d1f76740.ngrok.io/update_points"


def check_if_game_today():

    today = datetime.now()

    if today.month == 12:
        idx = 0

    #edge case, if the game goes into next day...
    if today.hour < 3:
        today = today - timedelta(1)
        today.replace(hour = 23, minute = 59)

    get_url = "https://ca.global.nba.com/stats2/team/schedule.json?countryCode=CA&locale=en&teamCode=lakers"
    #get_url = "https://ca.global.nba.com/stats2/team/schedule.json?countryCode=CA&locale=en&teamCode=bucks"
    
    data = requests.get(get_url).json() 
    data = data['payload']['monthGroups'][idx]['games']

    game_ID = None

    for row in data:
        game_date = row['profile']['dateTimeEt']

        game_date = datetime.strptime(game_date, "%Y-%m-%dT%H:%M")
        #game_len = row['boxscore']['gameLength']

        game_status = row['boxscore']['statusDesc']
        # 'Final' = game done
        # 'period # = game ongoing
        # Null = game not started

        if game_date.day == today.day:
            print("there is a game today")

            if game_status:
                print("game has started", game_date.hour, game_date.minute, game_status)
                game_ID = row['profile']['gameId']
                return game_ID
            else:
                print("game not started")
                return game_ID

            
    print("there is no game today")    
    return game_ID


def get_player_static_pts(player_ID):
    get_url = "https://stats.nba.com/stats/leagueLeaders?ActiveFlag=No&LeagueID=00&PerMode=Totals&Scope=S&Season=All+Time&SeasonType=Regular+Season&StatCategory=PTS"

    data = requests.get(get_url).json() 

    for row in data['resultSet']['rowSet']:
        if row[0] == int(player_ID):
            total_pts = row[21]
            break

    return total_pts


def get_player_live_pts(game_ID, player_ID):

    get_url = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{}.json".format(game_ID)
    print(get_url)
     
    try:
        data = requests.get(get_url).json()
        return json_extract(data,'personId', 'points', player_ID)
    except:
        print("game hasn't started yet")
        return 0


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

                #Find Lebron
                elif k == key and v == int(player_ID): 
                    #print("we found him", v)
                    save_flag = True

                #Save his points
                elif k == key2 and save_flag:
                    #print("save points", v)
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

    game_id = check_if_game_today()
    lebron_live_points = 0

    if game_id:
        print("There is a game on - LIVE UPDATE - {}".format(game_id))
        lebron_live_points = get_player_live_pts(game_ID = game_id, player_ID = lebron_player_id)
    else:
        print("There is no game on - STATIC POINTS ONLY")
    
    # Need a condition that stops live updating a certain amount of time after
    # the games is finished, otherwise might have a case where the "static" score is updated
    # while it's still adding the "live" score from the finished game. Need to get a sense of
    # how soon after a game is done that the "static" score is updated

    lebron_static_points = get_player_static_pts(player_ID=lebron_player_id)
    
    print("static points = {}, live points = {}\n".format(lebron_static_points, lebron_live_points))

    return str(max(0, kareem_static_points - (lebron_static_points + lebron_live_points)))


def fetch_lebron_points_countdown_local():
    return requests.get(local_proxy).text


def lebron_points_countdown():
    cache_invalidation_time = datetime.now() - timedelta(seconds=cache_refresh_seconds)

    if _cache.get("timestamp", datetime.min) < cache_invalidation_time:
        _cache.update(
            {"timestamp": datetime.now(), "points": fetch_lebron_points_countdown()}
        )

    return _cache["points"]

