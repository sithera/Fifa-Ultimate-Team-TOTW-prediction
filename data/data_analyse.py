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

class DataAnalyzer(object):
    def __init__(self, db='statistics.db'):
        self.conn = sqlite3.connect('statistics.db')
        self.rows = []
        self.X = []
        self.Y = [] # id, date, fixture, statistics, if in 11 of the week
        self.pca_variance = []
    
    def fetch_data(self, table='player_statistics'):
        with self.conn:
            cursor = self.conn.cursor()    
            cursor.execute("SELECT * FROM " + str(table))
            while True:      
                row = cursor.fetchone()
                if row == None:
                    break
                self.rows.append(row)
    
    def run_PCA(self):
        self.X = np.array([list(self.rows[x][5:]) for x in range(len(self.rows))])
        pca = PCA(n_components=3)
        pca.fit(self.X)
        self.pca_variance = pca.explained_variance_ratio_
        self.Y = pca.transform(self.X)
        print self.rows[1]

        ids = [self.rows[i][0] for i in range(len(self.rows))]
        date = [self.rows[i][3] for i in range(len(self.rows))]
        fixtures = [self.rows[i][4] for i in range(len(self.rows))]
        #statistics = self.Y[i].tolist()
        if_in_TOtW = 0
        self.Y = [[ids[i]] + [date[i]] + [fixtures[i]] + self.Y[i].tolist() + [if_in_TOtW] for i in range(len(self.Y))]
        #print self.Y
        mylist = filter(lambda x : x[0] == 3965, self.Y)
        #print mylist

    def handle_json(self, year, fixture, filename='team_of_the_week.json'):
        with open(filename) as data_file:
            data = json.load(data_file)
            #print data["data"]
            #pprint(data[0]["data"][fixture-1]["fixture"])
            #pprint(data[0]["data"][fixture-1]["players"])

        return data[year-2015]["data"][fixture-1]["players"]

    def find_player_id(self, name):
        #print [self.rows[i] for i in range(len(self.rows))]
        player_data = filter(lambda x : x[1] == name, [self.rows[i] for i in range(len(self.rows))])
        return player_data[0][0]

    def update_if_in_TOtw(self, year, fixture):
        data = self.handle_json(year, fixture)
        players = []
        for position in data[0]:
            for player in data[0][position]:
                players.append(player)
        print players
        for player in players:
            id = self.find_player_id(player)
            matches = [match for match in self.find_element(id)]
            candidates = self.prepare_candidates(matches)
            candidates = self.slice_by_fixture(candidates, fixture)
            candidates = self.slice_by_season(candidates, year)
            #try:

            self.Y[candidates[0][-1]][-1] = 1 # is in team of the week
            #except IndexError:
            #    pass
            #continue
            
            print "candidate ostateczny: " + str(self.Y[candidates[0][7]])
            #print "candidate ostateczny self Y: " + str(self.Y[candidates[0][7]][6])
            
    def find_element(self, id):
        for i, player in enumerate(self.Y):
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
        return filter(lambda x : datetime.strptime(x[1], '%Y-%m-%d') > datetime(start_year, 7,7) and datetime.strptime(x[1], '%Y-%m-%d') < datetime(start_year+1, 7, 7), candidates)

    def update_all_players(self, year):
        fixtures = range(36,37)
        for i in fixtures:
            self.update_if_in_TOtw(year, i)
        self.save_to_file('data_calculated' + str(year), self.Y)

    def save_to_file(self, filename, content):
        filename = filename + ".csv"
        with open(filename, 'wb') as file:
            writer = csv.writer(file)
            #print content
            #print type(content)
            for i in content:
                print i

                writer.writerow(i)
            #file.write(content)

    #spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    #spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    def run_svm(self):
        Xsvm = []
        ysvm = []
        for i in range(len(self.Y)):
            if i < 100:
                continue
            Xsvm.append(self.Y[i][3:6])
            print self.Y[i][3:6]
            ysvm.append(self.Y[i][6])

        #print Xsvm
        #print ysvm


        clf = svm.SVC()
        clf.fit(Xsvm,ysvm)

        print clf.predict([[95.46998874785378,	-10.455099879722816,	8.249285784045766]])
        print clf.predict([[-11.911608306775511,	-4.960642606125528,	-21.248186559307268]])
        print clf.predict([[-84.96169891257794,	14.995920700196903,	16.34380187691025]])
        print clf.predict([[-61.5396615043822,	-4.719625078226473,	0.9947794822283846]])
        print clf.predict([[49.17837859606411,	33.93099009166503,	-3.2989638896094835]])
        print clf.predict([[-36.088040844332426,	-16.437124809782212,	-23.30283250693931]])
        print clf.predict([[23.071458306015284,	6.3895150724014504,	-15.641327844575892]])
        print clf.predict([[0.5474392044500311,	19.583617357003405,	-13.070166080634563]])
        print clf.predict([[125.79422002401283,	81.08243862949172,	-15.579239375631678]])
        print clf.predict([[-58.92553677984468,	-5.709797335438783,	-19.555997730779442]])
        print clf.predict([[134.87989156562023,	-51.14799314269806,	44.93611270473487]])



    
if __name__ == "__main__":
    data = DataAnalyzer()
    data.fetch_data()
    #print data.rows
    data.run_PCA()
    print "PCA variance for 3 components: {0}".format(data.pca_variance)
    print "Sum of first 3 PCA components: {0}".format(sum(data.pca_variance))

    #data.handle_json(2)
    #data.find_player_id('Ashley Fletcher')
    #print data.Y
    #data.slice_by_season(2015)
	
    data.update_all_players(2016)
    data.run_svm()
    #print "plaers ids"
    #print data.find_player_id("Michael Keane")
    

