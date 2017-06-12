import requests
from DBHandler import DBHandler


class PlayersPositionFeeder(object):
    def __init__(self):
        self.headers = requests.utils.default_headers()
        self.headers.update(
            {
                'User-Agent': 'Mozilla/5.0',
            }
        )
        self.db_handler = DBHandler()

    def populate_players_positions(self, match_id):
        position_feed_url = "http://data.champdas.com/getMatchPersonAjax.html"
        players_feed = requests.post(position_feed_url, headers=self.headers, timeout=20, data={'matchId': match_id})
        for player_feed in players_feed.json():
            if repr(player_feed['personPosition']) == "u'\u95e8\u5c06'":
                self.db_handler.update_player_position("gk", player_feed['personId'])
            elif repr(player_feed['personPosition']) == "u'\u540e\u536b'":
                self.db_handler.update_player_position("def", player_feed['personId'])
            elif repr(player_feed['personPosition']) == "u'\u4e2d\u573a'":
                self.db_handler.update_player_position("mid", player_feed['personId'])
            elif repr(player_feed['personPosition']) == "u'\u524d\u950b'":
                self.db_handler.update_player_position("att", player_feed['personId'])
