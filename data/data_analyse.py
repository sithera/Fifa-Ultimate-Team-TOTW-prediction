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

class DataAnalyzer(object):
    def __init__(self):
        self.conn = sqlite3.connect('statistics.db')
        self.rows = []
        self.players = []
        self.X = []
        self.Y = []  # id, date, fixture, statistics, if in team of the week
        self.pca_variance = []
        self.splitted_data = {}
        self.training_set = []
    
    def fetch_data(self, table1='player', table2='player_statistics'):
        with self.conn:
            cursor = self.conn.cursor()    
            cursor.execute("SELECT * FROM {0} JOIN {1} ON {0}.player_id = {1}.player_id;".format(str(table1), str(table2)))
            while True:      
                row = cursor.fetchone()
                if row is None:
                    break
                self.rows.append(row)

    def split_data_by_position(self, position):
        # player_data = filter(lambda x: x[1] == name, [self.rows[i] for i in range(len(self.rows))])
        #print self.Y[0]
        #print self.rows[0]
        #print self.training_set[0]
        self.splitted_data["GK"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][2] == "gk"]
        print "Y przed:"
        print self.Y[0]
        self.splitted_data["GK"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][2] == "gk"]
        print self.splitted_data["GK"][0]
        print "po"
        print [a[-1] for a in self.Y if a[-1]]
        print [a[-1] for a in self.splitted_data["GK"] if a[-1]]
        for a in self.splitted_data["GK"]:
            if a[-1]:
                print a[-1]
        self.splitted_data["DEF"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][2] == "def"]
        self.splitted_data["MID"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][2] == "mid"]
        self.splitted_data["ATT"] = [self.Y[i] for i in range(len(self.Y)) if self.rows[i][2] == "att"]


        # print self.splitted_data["GK"]
        self.splitted_data["DEF"] = filter(lambda x: x[2] == "def", [self.Y[i] for i in range(len(self.rows))])
        self.splitted_data["MID"] = filter(lambda x: x[2] == "mid", [self.Y[i] for i in range(len(self.rows))])
        self.splitted_data["ATT"] = filter(lambda x: x[2] == "att", [self.Y[i] for i in range(len(self.rows))])
        self.training_set = filter(lambda x: x[2] == position.lower(), [self.training_set[i] for i in range(len(self.training_set))])
        return self.training_set

    def prepare_features(self, position, features_start_index=8):
        #self.training_set = self.splitted_data[position]
        self.training_set = self.rows
        self.X = np.array([list(self.training_set[x][features_start_index:]) for x in range(len(self.training_set))])
        self.Y = self.X

    def run_pca(self):
        pca = PCA(n_components=3)
        pca.fit(self.X)
        self.pca_variance = pca.explained_variance_ratio_
        self.Y = pca.transform(self.X)

    def prepare_y(self):
        range_training_set = range(len(self.training_set))
        id_column, date_column, fixture_column = 3, 6, 7
        ids = [self.training_set[i][id_column] for i in range_training_set]
        date = [self.training_set[i][date_column] for i in range_training_set]
        fixtures = [self.training_set[i][fixture_column] for i in range_training_set]
        if_in_totw = 0
        self.Y = [[ids[i]] + [date[i]] + [fixtures[i]] + self.Y[i].tolist() + [if_in_totw] for i in range(len(self.training_set))]

    def update_all_players(self, year, position):
        fixtures = range(1, 37)
        for i in fixtures:
            self.update_if_player_in_totw(year, i, position)
        self.save_to_file('data_calculated{}{}'.format(str(year), position), self.Y)

        print "marian"


    def update_if_player_in_totw(self, year, fixture, position):
        positions = self.handle_json(year, fixture)
        # players = self.handle_json(year, fixture, position)
        players = []
        for position in positions[0]:
            for player in positions[0][position]:
                players.append(player)

        for player in players:
            id = self.find_player_id(player)
            print player, id

            matches = [match for match in self.find_element(id)]
            candidates = self.prepare_candidates(matches)
            print player, id, candidates
            print player, id, matches
            candidates = self.slice_by_fixture(candidates, fixture)
            print player, id, candidates
            candidates = self.slice_by_season(candidates, year)
            print player, id, candidates
            # print self.Y

            self.Y[candidates[0][-1]][-1] = 1  # is in team of the week

            print "candidate ostateczny: " + str(self.Y[candidates[0][-1]])
            # print "candidate ostateczny self Y: " + str(self.Y[candidates[0][7]][6])

    def handle_json(self, year, fixture, filename='team_of_the_week.json'):
        with open(filename) as f:
            json_data = json.load(f)
        first_year = 2015
        return json_data[year-first_year]["data"][fixture-1]["players"]

    def handle_json_by_position(self, year, fixture, position, filename='team_of_the_week.json'):
        with open(filename) as f:
            json_data = json.load(f)
        first_year = 2015
        return json_data[year-first_year]["data"][fixture-1]["players"][0][position]

    def find_player_id(self, name):
        #print [self.rows[i] for i in range(len(self.rows))]
        print name
        print self.rows[0]
        player_data = filter(lambda x: x[0] == name, [self.rows[i] for i in range(len(self.rows))])
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
        return filter(lambda x : datetime(start_year+1, 7, 7) > datetime.strptime(x[1], '%Y-%m-%d') > datetime(start_year, 7,7), candidates)

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

    def run_svm(self):
        print len(self.training_set)
        #for i in range(len(self.training_set)):
        #    print self.Y[i][-1]

        #for i in range(len(self.training_set)):
            #X.append(self.training_set[i][8:-1])
            # print self.training_set[i][8:-1]
            # print self.training_set[i][3:6]
         #   ysvm.append(self.training_set[i][-1])

        #print Xsvm
        #print ysvm
        xtrain, ytrain, xtest, ytest = self.split_data()

        clf = svm.SVC(kernel='linear')
        print clf.fit(xtrain, ytrain)
        # print clf.score(xtest, ytest)
        y_pred = clf.predict(xtest)
        print confusion_matrix(ytest, y_pred)

    def split_data(self):
        xtrain = []
        ytrain = []
        xtest = []
        ytest = []

        for j, i in enumerate(self.training_set):
            # print j
            if j % 4 != 0:
                xtrain.append(i[8:-1])
                ytrain.append(i[-1])
            else:
                xtest.append(i[8:-1])
                ytest.append(i[-1])
        print "here "
        print [x for x in ytrain if x]
        return xtrain, ytrain, xtest, ytest




    
if __name__ == "__main__":
    data = DataAnalyzer()
    data.fetch_data()
    # print data.rows
    position = "GK"
    data.prepare_features(position)
    data.prepare_y()
    # data.run_PCA()
    # print "PCA variance for 3 components: {0}".format(data.pca_variance)
    # print "Sum of first 3 PCA components: {0}".format(sum(data.pca_variance))

    #data.handle_json(2)
    #data.find_player_id('Ashley Fletcher')
    #print data.Y
    #data.slice_by_season(2015)

    data.update_all_players(2016, position)
    data.split_data_by_position("att")
    # print [x for x in data.splitted_data["GK"] if x[0] == 4378]
    print [x[-1] for x in data.splitted_data["DEF"] if x[-1]]
    print [x[-1] for x in data.splitted_data["MID"] if x[-1]]
    print [x[-1] for x in data.splitted_data["ATT"] if x[-1]]

    # data.run_svm()
    #print "plaers ids"
    #print data.find_player_id("Michael Keane")
    

