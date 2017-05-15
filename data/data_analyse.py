#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import sys
import numpy as np
from sklearn.decomposition import PCA

class DataAnalyzer(object):
    def __init__(self, db='statistics.db'):
        self.conn = sqlite3.connect('statistics.db')
        self.rows = []
        self.X = []
        self.Y = []
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
    
if __name__ == "__main__":
	data = DataAnalyzer()
	data.fetch_data()
	data.run_PCA()
	print "PCA variance for 3 components: {0}".format(data.pca_variance)
	print "Sum of first 3 PCA components: {0}".format(sum(data.pca_variance))
	