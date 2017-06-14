import sqlite3
from sklearn import svm
import csv
from datetime import datetime
from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN
from sklearn import linear_model
import numpy as np


class Analysis(object):

    def __init__(self, fixture, year, position):
        self.fixture = fixture
        self.year = year
        self.position = position
        self.original_data = []
        self.train_data = []
        self.test_data = []
        self.filename = ""
        self.set_filename()
        self.X_train = []
        self.X_test = []
        self.y_train = []
        self.y_test = []

    def set_filename(self):
        self.filename = "data_calculated{}{}.csv".format(self.year, self.position)

    def read_original_data(self):
        with open(self.filename, 'rb') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                row = [int(i) if "-" not in i else i for i in row]
                self.original_data.append(row)

    def run_svm(self):
        clf = svm.SVC(kernel='linear', probability=True)
        print "classification done"
        print clf.fit(self.X_train, self.y_train)
        print "fit done"
        print "score: {}".format(clf.score(self.X_test, self.y_test))
        y_pred = clf.predict_proba(self.X_test)
        self.save_to_files(y_pred)

    def run_lasso(self):
        clf = linear_model.Lasso(alpha=0.1)
        print "classification done"
        clf.fit(self.X_train, self.y_train)
        print "fit done"
        y_pred = clf.predict(self.X_test)
        self.save_to_files(y_pred, "lasso")

    def save_to_files(self, y_pred, method=""):
        players = []
        for i in range(len(self.test_data)):
            players.append(self.test_data[i][:3])
        print players
        print y_pred
        self.save_to_file("results{}{}{}".format(self.year, self.position, self.fixture), players, method)
        self.save_to_file("predicted{}{}{}".format(self.year, self.position, self.fixture), y_pred, method)
        results = zip(players, y_pred)
        print results
        combined = []
        for i in results:
            if method == "lasso":
                i[1] = [i[1]]
        self.save_to_file("combined{}{}{}".format(self.year, self.position, self.fixture), combined, method)

    def extract_data(self):
        self.X_train = [self.train_data[i][3:-1] for i in range(len(self.train_data))]
        self.y_train = [self.train_data[i][-1] for i in range(len(self.train_data))]
        self.X_test = [self.test_data[i][3:-1] for i in range(len(self.test_data))]
        self.y_test = [self.test_data[i][-1] for i in range(len(self.test_data))]

    def save_to_file(self, filename, content, method=""):
        if method:
            filename = filename + method + ".csv"
        else:
            filename = filename + ".csv"
        with open(filename, 'wb') as f:
            writer = csv.writer(f)
            for i in content:
                if type(i) == np.float64:
                    i = [i]
                writer.writerow(i)

    def oversample(self):
        # X_train, y_train = self.oversample_data(X_train, y_train)
        self.X_train, self.y_train = self.smote(self.X_train, self.y_train)
        # X_train, y_train = self.adasyn(X_train, y_train)

    def oversample_data(self, X, y):
        ros = RandomOverSampler()
        X_resampled, y_resampled = ros.fit_sample(X, y)
        return X_resampled, y_resampled

    def smote(self, X, y):
        X_resampled, y_resampled = SMOTE().fit_sample(X, y)
        return X_resampled, y_resampled

    def adasyn(self, X, y):
        ada = ADASYN()
        X_resampled, y_resampled = ada.fit_sample(X, y)
        return X_resampled, y_resampled

    def slice_sets(self):
        for i in self.original_data:
            if i[2] == self.fixture and datetime(self.year + 1, 7, 7) > datetime.strptime(i[1], '%Y-%m-%d') > datetime(self.year, 7, 7):
                self.test_data.append(i)
            else:
                self.train_data.append(i)

if __name__ == "__main__":
    fixture_test = 30
    year_test = 2016
    positions = ["GK", "DEF", "MID", "ATT"]

    for position in positions:
        data = Analysis(fixture_test, year_test, position)
        data.read_original_data()
        data.slice_sets()
        data.extract_data()
        data.oversample()
        data.run_lasso()
        print "done {}".format(position)

