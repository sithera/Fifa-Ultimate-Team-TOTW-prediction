from PlayersDataFetcher import PlayersDataFetcher
from DBHandler import DBHandler


def main_func():
    fetcher = PlayersDataFetcher("PremierLeague", 2016, 1)
    matches = fetcher.get_all_fixture_matches()
    fetcher.populate_players_statistics_from_match(matches[0])


def players():
    db = DBHandler()
    return db.get_all_players()


if __name__ == "__main__":
    main_func()
