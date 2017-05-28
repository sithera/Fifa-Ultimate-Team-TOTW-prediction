from PlayersDataFetcher import PlayersDataFetcher
from DBHandler import DBHandler

import json

if __name__ == "__main__":
    # for league in ['PremierLeague', 'LaLiga']:
    #     print "League: " + league
    #     for year_num in range(2014, 2017):
    #         print "Year: " + str(year_num)
    #         for fixture_num in range(1, 39):
    #             print "Fixture: " + str(fixture_num)
    #             fetcher = PlayersDataFetcher(league, year_num, fixture_num)
    #             matches = fetcher.get_all_fixture_matches()
    #             for match in matches:
    #                 fetcher.populate_players_statistics_from_match(match)
    handler = DBHandler()

    with open('team_of_the_week.json') as json_data:
        data = json.load(json_data)
        for fixture_data in data['data']:
            for player in fixture_data['players'][0]['GK']:
                handler.check_player_name(player)
            for player in fixture_data['players'][0]['DEF']:
                handler.check_player_name(player)
            for player in fixture_data['players'][0]['MID']:
                handler.check_player_name(player)
            for player in fixture_data['players'][0]['ATT']:
                handler.check_player_name(player)
