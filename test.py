import requests
from lxml.html import fromstring

from nba_api.stats.endpoints.alltimeleadersgrids import AllTimeLeadersGrids
from nba_api.stats.endpoints.playercareerstats import PlayerCareerStats

# from nba_api.stats.endpoints import commonplayerinfo
# from nba_api.stats.static import players


kareem_player_id = "76003"
lebron_player_id = "2544"

cache_refresh_seconds = 5

_cache = {}


def get_proxies(srch_len):
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()

    for i in parser.xpath("//tbody/tr")[:srch_len]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            # Grabbing IP and corresponding PORT
            proxy = ":".join(
                [i.xpath(".//td[1]/text()")[0], i.xpath(".//td[2]/text()")[0]]
            )

            proxies.add(proxy)
    return proxies


def check_proxies(proxies):
    saved_proxies = []

    url = "https://httpbin.org/ip"
    for i, proxy in enumerate(proxies):
        # Get a proxy from the pool
        print("Request #%d" % (i + 1))
        try:
            print(proxy)
            response = requests.get(
                url, proxies={"http": proxy, "https": proxy}, timeout=0.5
            )
            print(response.json())
            saved_proxies.append(proxy)
        except:
            print("Skipping. Connnection error")

    return saved_proxies


def get_stat_data(working_proxies):
    aa = None
    for i, one_proxy in enumerate(working_proxies):
        # Get a proxy from the pool
        print("Request #%d" % (i + 1))
        try:
            print(one_proxy)
            aa = AllTimeLeadersGrids(
                proxy=one_proxy, timeout=2
            ).pts_leaders.get_data_frame()
            return aa
        except:
            print("Skipping. Connnection error")

    if aa is None:
        print("dont use proxy")
        aa = AllTimeLeadersGrids().pts_leaders.get_data_frame()
        return aa


def get_player_total_pts(id_num):

    bb = PlayerCareerStats
    career = PlayerCareerStats(player_id=id_num)
    totals_reg = career.career_totals_regular_season
    total_pts = totals_reg.get_data_frame()["PTS"][0]

    return total_pts


def fetch_lebron_points_countdown():
    """On the road to become number 1, only Kareem to pass!"""
    # lebron_total_points = get_player_total_pts(id_num=lebron_player_id)
    # kareem_total_points = get_player_total_pts(id_num=kareem_player_id)

    # lebron_total_points = players.find_players_by_first_name('lebron' )[0]["id"]
    # kareem_total_points = players.find_players_by_first_name('kareem')[0]["id"]

    proxies = get_proxies(50)
    print("Total proxies\n", proxies, "\n")

    working_proxies = check_proxies(proxies)
    print("\nWorking proxies\n", working_proxies, "\n")

    api_data = get_stat_data(working_proxies)
    print(api_data)

    kareem_total_points = api_data.loc[
        api_data["PLAYER_ID"] == int(kareem_player_id), "PTS"
    ].iloc[0]
    lebron_total_points = api_data.loc[
        api_data["PLAYER_ID"] == int(lebron_player_id), "PTS"
    ].iloc[0]

    return str(max(0, kareem_total_points - lebron_total_points))


if __name__ == "__main__":
    a = fetch_lebron_points_countdown()
    print(a)
