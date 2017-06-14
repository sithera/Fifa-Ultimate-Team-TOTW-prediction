#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import numpy as np
from sklearn.decomposition import PCA
import json
import csv
from datetime import datetime
from DBHandler import DBHandler


class DataPreparation(object):
    def __init__(self):
        self.dbhandler = DBHandler()
        self.rows = []
        self.players = []
        self.X = []
        self.Y = []  # id, date, fixture, statistics, if in team of the week
        self.pca_variance = []
        self.splitted_data = {}

    def fetch_data(self):
        self.rows = self.dbhandler.get_all_players_with_positions_and_statistics()

    def prepare_features(self, features_start_index=6):
        self.X = np.array([list(self.rows[x][features_start_index:]) for x in range(len(self.rows))])
        self.Y = self.X

    def run_pca(self):
        pca = PCA(n_components=3)
        pca.fit(self.X)
        self.pca_variance = pca.explained_variance_ratio_
        self.Y = pca.transform(self.X)

    def prepare_y(self):
        range_training_set = range(len(self.rows))
        id_column, date_column, fixture_column = 1, 4, 5
        ids = [self.rows[i][id_column] for i in range_training_set]
        date = [self.rows[i][date_column] for i in range_training_set]
        fixtures = [self.rows[i][fixture_column] for i in range_training_set]
        if_in_totw = 0
        self.Y = [[ids[i]] + [date[i]] + [fixtures[i]] + self.Y[i].tolist() + [if_in_totw] for i in range(len(self.rows))]

    def update_all_players(self, year):
        fixtures = range(1, 39)
        for i in fixtures:
            self.update_if_player_in_totw(year, i)
        self.save_to_file('data_calculated{}'.format(str(year)), self.Y)

    def update_if_player_in_totw(self, year, fixture):
        positions = self.handle_json(year, fixture)
        # players = self.handle_json(year, fixture, position)
        players = []
        for p in positions[0]:
            for player in positions[0][p]:
                players.append(player)

        for player in players:
            id = self.find_player_id(player)

            matches = [match for match in self.find_element(id)]
            candidates = self.prepare_candidates(matches)
            candidates = self.slice_by_fixture(candidates, fixture)
            candidates = self.slice_by_season(candidates, year)
            self.Y[candidates[0][-1]][-1] = 1  # is in team of the week

    def handle_json(self, year, fixture, filename='team_of_the_week.json'):
        with open(filename) as f:
            json_data = json.load(f)
        first_year = 2015
        return json_data[year-first_year]["data"][fixture-1]["players"]

    def find_player_id(self, name):
        player_data = filter(lambda x: x[2] == name, [self.rows[i] for i in range(len(self.rows))])
        return player_data[0][1]

    def find_element(self, id):
        for i, player in enumerate(self.rows):
            try:
                j = player.index(id)
            except ValueError:
                continue
            yield i

    def prepare_candidates(self, matches):
        candidates = []
        for i in matches:
            record = self.Y[i] + [i]
            candidates.append(record)
        return candidates

    def slice_by_fixture(self, candidates, fixture):
        return filter(lambda x: x[2] == fixture, candidates)

    def slice_by_season(self, candidates, start_year):
        return filter(lambda x: datetime(start_year+1, 7, 7) > datetime.strptime(x[1], '%Y-%m-%d') >
                                datetime(start_year, 7, 7), candidates)

    def save_to_file(self, filename, content):
        filename = filename + ".csv"
        with open(filename, 'wb') as file:
            writer = csv.writer(file)
            for i in content:
                writer.writerow(i)

    def split_data_by_position(self, year):
        positions = ["GK", "DEF", "MID", "ATT"]
        for position in positions:
            self.splitted_data[position] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][0].encode('utf8') == position.lower()]
            self.save_to_file('data_calculated{}{}'.format(str(year), position), self.splitted_data[position])

    
if __name__ == "__main__":
    data = DataPreparation()
    data.fetch_data()
    data.prepare_features()
    data.prepare_y()
    year = 2016
    data.update_all_players(year)
    data.split_data_by_position(year)
