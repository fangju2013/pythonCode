# -*- coding: utf-8 -*-

from __future__ import division
from ranktree import stree
import numpy as np

class Sgbt():
    def __init__(self ,depth ,minisamp ,precise ,rounds ,eta ,fittype='lg' ,earlystop = 0.00000001):
        self.rounds = rounds
        self.eta = eta
        self.forest = {}
        self.train_score = []
        self.test_score = []
        self.fittype = fittype
        self.maxdepth = depth
        self.minisamp = minisamp
        self.precise = precise
        self.earlystop = earlystop

    def fit(self, X_train , y_train):
        y_train[y_train == 0] = -1
        tmp = np.mean(y_train)
        self.f0 = self.eta * np.log((1 + tmp) / (1 - tmp)) / 2
        self.f = np.repeat(self.f0 ,len(X_train))
        for rd in np.arange(self.rounds):
            resiY = 2* y_train / (1 + np.exp(2 * y_train * self.f))
            meanresiy = np.mean(np.abs(resiY))
            if meanresiy < self.earlystop:
                print(rd)
                break
            slf = stree(depth=self.maxdepth, minisamp=self.minisamp, precise=self.precise, fitfunc=self.fittype)
            self.forest[rd], fity = slf.fit(X_train, resiY)
            self.f += self.eta * fity

    def predict(self, X):
        predy = self.f0.copy()
        for slf in self.forest.values():
            y = slf.predict(X)
            predy += y
        return self.eta * predy