import requests


class PlayersPositionFeeder(object):
    @staticmethod
    def populate_players_positions(name):
        position_feed_url = "http://www.easports.com/fifa/ultimate-team/api/fut/item?jsonParamObject={name:{}}".format(name)
        position_feed = requests.get(position_feed_url)

        print position_feed.json()