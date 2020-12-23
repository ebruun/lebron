from datetime import datetime, timedelta

import requests
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats
from nba_api.stats.endpoints.boxscoreadvancedv2 import BoxScoreAdvancedV2 as box
#from nba_api.stats.endpoints.boxscoreplayertrackv2 import BoxScorePlayerTrackV2 as box



from nba_api.stats.endpoints.leaguegamelog import LeagueGameLog

#b = BoxScoreAdvancedV2(1)

b = LeagueGameLog(season= '2020-21', league_id= '00' ,season_type_all_star= 'Regular Season').league_game_log
print(b.get_data_frame())

c = box('0022000001').player_stats
print(c.get_data_frame())