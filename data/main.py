from PlayersDataFetcher import PlayersDataFetcher
from DBHandler import DBHandler

if __name__ == "__main__":
    fetcher = PlayersDataFetcher("PremierLeague", 2016, 1)
    matches = fetcher.get_all_fixture_matches()
    fetcher.populate_players_statistics_from_match(matches[0])
    db = DBHandler()
    db.get_all_players()
