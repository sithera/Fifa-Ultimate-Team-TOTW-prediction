import urllib
from datetime import datetime
from bs4 import BeautifulSoup
import re
import requests
from DBHandler import DBHandler


class PlayersDataFetcher(object):
    leagues = {
        "LaLiga": 12,
        "PremierLeague": 14
    }

    def __init__(self, league, year, fixture):
        self.league = self.leagues[league]
        self.fixture = fixture
        self.db_handler = DBHandler()
        self.fixture_matches_url = "http://data.champdas.com/match/scheduleDetail-{}-{}-{}.html"\
            .format(self.league, year, fixture)

    def get_all_fixture_matches(self):
        result_matches = []
        r = urllib.urlopen(self.fixture_matches_url).read()
        soup = BeautifulSoup(r, 'html.parser')
        matches_container = soup.find("div", class_="against").find_next('ul').find_all('li')
        for match in matches_container:
            match_date = datetime.strptime(match.find('p').string, '%Y-%m-%d %H:%M')
            match_id = match.find('span', class_="matchNote").find_next('a', href=True)['href']
            result_matches.append({
                "id": self.parse_match_id(match_id),
                "date": match_date.date()
            })

        return result_matches

    @staticmethod
    def parse_match_id(text):
        obj = re.match(r'/match/data-(\d{4}).html', text)
        return obj.group(1)

    def populate_players_statistics_from_match(self, match):
        data_feed_url = "http://data.champdas.com/getMatchPersonAjax.html"
        players_feed = requests.post(data_feed_url, data={'matchId': match['id']})
        for player_feed in players_feed.json():
            player_feed['fixture'] = self.fixture
            player_feed['match_date'] = str(match['date'])
            self.db_handler.insert_player_statistics(player_feed)

