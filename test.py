from datetime import datetime, timedelta, date

import requests

from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2 as box

from nba_api.stats.endpoints.playernextngames import PlayerNextNGames

from nba_api.stats.static import players


id = '2544' #LeBron
#id = '203507' #Giannis

# def check_if_game_today():

#     today = date.today()
#     diff = timedelta(0)
#     today = (today- diff).strftime('%b %d, %Y').upper()

#     df = PlayerNextNGames(player_id = id, number_of_games=5).next_n_games.get_data_frame()

#     df_today = df.loc[(df['GAME_DATE'] == today)]

#     print(df_today)

#     if df_today.empty:
#         print("No Game Today")

#         #just for testing
#         game_ID = '0022000002' 
#         game_TIME = None
#         #game_ID = False
#         #game_TIME = False
#     else:
#         print("There is a Game Today")
#         game_ID = df_today['GAME_ID'].values[0]
#         game_TIME = df_today['GAME_TIME'].values[0]    
        
#     return (game_ID, game_TIME)



def get_player_dynamic_pts(game_ID):
    get_url = "https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game}.json".format(game = game_ID)

    print(get_url)
    try:
        data = requests.get(get_url).json()
        return data
    except:
        print("game hasn't started yet")
        data = None
        return data

def get_player_static_pts(player_ID):
    get_url = "https://stats.nba.com/stats/leagueLeaders?ActiveFlag=No&LeagueID=00&PerMode=Totals&Scope=S&Season=All+Time&SeasonType=Regular+Season&StatCategory=PTS"

    data = requests.get(get_url).json() 

    for row in data['resultSet']['rowSet']:
        if row[0] == int(player_ID):
            total_pts = row[21]
            break

    return total_pts


def check_if_game_today():

    today = datetime.now()

    idx = today.month

    if idx == 12:
        idx = 0

    get_url = "https://ca.global.nba.com/stats2/team/schedule.json?countryCode=CA&locale=en&teamCode=lakers"

    data = requests.get(get_url).json() 
    data = data['payload']['monthGroups'][idx]['games']

    game_ID = None

    for row in data:
        game_date = row['profile']['dateTimeEt']

        game_date = datetime.strptime(game_date, "%Y-%m-%dT%H:%M")
        game_len = row['boxscore']['gameLength']
 
        if game_date.day == today.day:
            print("there is a game today")

            if today.hour >= game_date.hour and today.minute >= game_date.minute:
                print("game started")
                game_ID = row['profile']['gameId']
                return game_ID
            else:
                print("game not started")
            

    print("there is no game today")    
    return game_ID



def json_extract(obj, key, key2, player_id):
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
                elif k == key and v == int(player_id): 
                    print("we found him")
                    save_flag = True
                #Save his points
                elif k == key2 and save_flag:
                    print("save points")
                    arr.append(v)
                    save_flag = False
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key, key2, save_flag)
        return arr

    values = extract(obj, arr, key, key2, save_flag)
    return values[0]

game_ID = check_if_game_today()


data = get_player_dynamic_pts(game_ID)
#points = json_extract(data,'personId', 'points',id)
#print(points)

points = get_player_static_pts(player_ID = id)
print(points)

