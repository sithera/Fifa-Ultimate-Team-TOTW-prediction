import csv
import re
from DBHandler import DBHandler
import json


class CombinedAnalysis(object):

    def __init__(self, fixture, year):
        self.fixture = fixture
        self.year = year
        self.players = {
            "GK": [],
            "DEF": [],
            "MID": [],
            "ATT": []
        }
        self.final_squad = self.players.copy()

    def read_file(self, position):
        filename = "combined{}{}{}.csv".format(self.year, position, self.fixture)
        with open(filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                row = [float(i) if not re.match(r'(\d+-\d+-\d+)', i) else i for i in row]
                self.players[position].append(row)

    def get_best_players(self, position):
        self.players[position].sort(key=lambda x: float(x[4]), reverse=True)
        if position is "GK":
            self.final_squad[position] = [int(self.players[position][0][0])]
        else:
            self.players[position] = [i for i in self.players[position][:5]]
            if position is "ATT":
                self.final_squad[position] = [i for i in self.players[position][:2]]
            else:
                self.final_squad[position] = [i for i in self.players[position][:3]]

    def prepare_final_squad(self):
        all_together = self.players["DEF"][3:] + self.players["MID"][3:] + self.players["ATT"][2:]
        all_together = all_together[:2]
        for player in all_together:
            position = self.find_position(player)
            self.final_squad[position].append(player)

    def cleanup_final_squad(self):
        positions = ["DEF", "MID", "ATT"]
        for position in positions:
            self.final_squad[position] = [int(x[0]) for x in self.final_squad[position]]

    def get_players_data(self):
        positions = ["GK", "DEF", "MID", "ATT"]
        dbhandler = DBHandler()
        for position in positions:
            self.final_squad[position] = [dbhandler.get_player_data_by_id(x) for x in self.final_squad[position]]

    def save_to_json(self, fixture):
        with open('../flaskr/flaskr/team_of_the_week{}.json'.format(fixture), 'w') as outfile:
            json.dump(self.final_squad, outfile)

    def find_position(self, record):
        player_id = record[0]
        for position in positions:
            if [i for i in self.players[position] if i[0] == player_id]:
                return position

if __name__ == "__main__":
    fixture_test = 30
    year_test = 2016
    data = CombinedAnalysis(fixture_test, year_test)
    positions = ["GK", "DEF", "MID", "ATT"]
    for position in positions:
        data.read_file(position)
        data.get_best_players(position)
    data.prepare_final_squad()
    data.cleanup_final_squad()
    data.get_players_data()
    data.save_to_json(fixture_test)
    print "done"

