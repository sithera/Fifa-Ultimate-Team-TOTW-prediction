from PlayersDataFetcher import PlayersDataFetcher

if __name__ == "__main__":
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
