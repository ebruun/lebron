from nba_api.stats.endpoints import commonplayerinfo
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players

def get_player_total_pts(id_num):
    p = players.find_player_by_id(id_num)

    career = playercareerstats.PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season

    total_pts = totals_reg.get_data_frame()["PTS"][0]

    #print(career.get_data_frames()[0])
    #print(a.get_data_frame())
    #print(a.get_data_frame()["PTS"])

    print('{} has {} points'.format(p['full_name'], total_pts))
    return total_pts
    
p1 = get_player_total_pts(76003) #KAREEM
p2 = get_player_total_pts(2544) #LEBRON

# write data in a file. 
f = open("./points_left.txt","w") 
f.write(str(p1 - p2))
f.close()