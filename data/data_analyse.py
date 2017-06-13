#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import numpy as np
from sklearn import svm
from sklearn.decomposition import PCA
import json
import csv
from pprint import pprint
from datetime import datetime
from collections import defaultdict
from itertools import chain
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split


class DataAnalyzer(object):
    def __init__(self):
        self.conn = sqlite3.connect('statistics.db')
        self.rows = []
        self.players = []
        self.X = []
        self.Y = []  # id, date, fixture, statistics, if in team of the week
        self.pca_variance = []
        self.splitted_data = {}

    def fetch_data(self, table1='player', table2='player_statistics'):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute("SELECT {0}.position, {1}.* FROM {0} JOIN {1} USING(player_id);".format(str(table1), str(table2)))
            while True:      
                row = cursor.fetchone()
                if row is None:
                    break
                self.rows.append(row)

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

            print "candidate ostateczny: " + str(self.Y[candidates[0][-1]])
            # print "candidate ostateczny self Y: " + str(self.Y[candidates[0][7]][6])

    def handle_json(self, year, fixture, filename='team_of_the_week.json'):
        with open(filename) as f:
            json_data = json.load(f)
        first_year = 2015
        return json_data[year-first_year]["data"][fixture-1]["players"]

    '''
    def handle_json_by_position(self, year, fixture, position, filename='team_of_the_week.json'):
        with open(filename) as f:
            json_data = json.load(f)
        first_year = 2015
        return json_data[year-first_year]["data"][fixture-1]["players"][0][position]
    '''

    def find_player_id(self, name):
        #print [self.rows[i] for i in range(len(self.rows))]
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
        return filter(lambda x: datetime(start_year+1, 7, 7) > datetime.strptime(x[1], '%Y-%m-%d') > datetime(start_year, 7,7), candidates)

    def save_to_file(self, filename, content):
        filename = filename + ".csv"
        with open(filename, 'wb') as file:
            writer = csv.writer(file)
            #print content
            #print type(content)
            for i in content:
            #    print i

                writer.writerow(i)
            #file.write(content)

    #spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    #spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    def split_data_by_position(self, year):
        # player_data = filter(lambda x: x[1] == name, [self.rows[i] for i in range(len(self.rows))])
        self.splitted_data["GK"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][0] == "gk"]
        self.save_to_file('data_calculated{}{}'.format(str(year), "GK"), self.splitted_data["GK"])
        self.splitted_data["DEF"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][0] == "def"]
        self.save_to_file('data_calculated{}{}'.format(str(year), "DEF"), self.splitted_data["DEF"])
        self.splitted_data["MID"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][0] == "mid"]
        self.save_to_file('data_calculated{}{}'.format(str(year), "MID"), self.splitted_data["MID"])
        self.splitted_data["ATT"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][0] == "att"]
        self.save_to_file('data_calculated{}{}'.format(str(year), "ATT"), self.splitted_data["ATT"])

        #self.splitted_data["DEF"] = filter(lambda x: x[2] == "def", [self.Y[i] for i in range(len(self.rows))])
        #self.splitted_data["MID"] = filter(lambda x: x[2] == "mid", [self.Y[i] for i in range(len(self.rows))])
        #self.splitted_data["ATT"] = filter(lambda x: x[2] == "att", [self.Y[i] for i in range(len(self.rows))])
        #self.rows = filter(lambda x: x[2] == position.lower(), [self.rows[i] for i in range(len(self.rows))])

    def run_svm(self, data_to_run):
        X_train, X_test, y_train, y_test = self.split_data(data_to_run)
        print len(X_train)
        print len(X_test)
        print len(y_train)
        print len(y_test)

        clf = svm.SVC(kernel='linear')
        #print X_train
        #print y_train
        print clf.fit(X_train, y_train)
        # print clf.score(xtest, ytest)
        y_pred = clf.predict(X_test)
        print confusion_matrix(y_test, y_pred)

    def split_data(self, data_to_split):
        data_ready_x = []
        data_ready_y = []
        print "cos {}".format(list(data_to_split)[0])
        for i in range(len(data_to_split)):
            data_ready_x.append(data_to_split[i][3:-1])
            data_ready_y.append(data_to_split[i][-1])
        print data_ready_x[0]
        print data_ready_x[1]
        X_train, X_test, y_train, y_test = train_test_split(data_ready_x, data_ready_y, test_size=0.33)
        return X_train, X_test, y_train, y_test


    
if __name__ == "__main__":
    '''
    data = DataAnalyzer()
    data.fetch_data()
    data.prepare_features()
    data.prepare_y()
    data.update_all_players(2016)
    data.split_data_by_position(2016)
    '''
    # filename = "data_calculated2016GK.csv"
    filename = "data_calculated2016DEF.csv"
    # filename = "data_calculated2016MID.csv"
    # filename = "data_calculated2016ATT.csv"
    data_to_analyse = []

    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',')
        counter = 0
        for row in reader:
            row = [int(i) for i in row if "-" not in i]
            data_to_analyse.append(row)

    data = DataAnalyzer()
    data.run_svm(data_to_analyse)


