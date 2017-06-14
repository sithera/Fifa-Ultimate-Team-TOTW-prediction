import json

import requests

from PlayersDataFetcher import PlayersDataFetcher
from DBHandler import DBHandler
from PlayersPositionFeeder import PlayersPositionFeeder


def load_players_data_into_database():
    for league in ['PremierLeague', 'LaLiga']:
        print "League: " + league
        for year_num in range(2014, 2017):
            print "Year: " + str(year_num)
            for fixture_num in range(1, 39):
                print "Fixture: " + str(fixture_num)
                fetcher = PlayersDataFetcher(league, year_num, fixture_num)
                matches = fetcher.get_all_fixture_matches()
                for match in matches:
                    fetcher.populate_players_statistics_from_match(match)


def check_players_names_in_database():
    with open('team_of_the_week.json') as json_data:
        data = json.load(json_data)
        for year in data:
            for fixture_data in year['data']:
                for player in fixture_data['players'][0]['GK']:
                    handler.check_player_name(player)
                for player in fixture_data['players'][0]['DEF']:
                    handler.check_player_name(player)
                for player in fixture_data['players'][0]['MID']:
                    handler.check_player_name(player)
                for player in fixture_data['players'][0]['ATT']:
                    handler.check_player_name(player)


def assign_position_to_each_player_in_database():
    for match in handler.get_all_matches_ids():
        print match[0]
        position_feeder.populate_players_positions(match[0])


def get_players_photos():
    for player in handler.get_all_players():
        id = player[1]
        name = player[0].split(" ")
        if len(name) > 1:
            name.pop(0)
        player_name = " ".join(name)
        api_url = 'http://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject={' \
                  '"name":"' + player_name + '"}'
        r = requests.get(api_url)
        items = r.json()['items']
        if len(items) == 0:
            print player_name
            continue
        img = items[0]['headshotImgUrl']
        handler.update_player_photo(img, id)


if __name__ == "__main__":
    handler = DBHandler()
    position_feeder = PlayersPositionFeeder()
