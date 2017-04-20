# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np

class stree():
    def __init__(self, depth=5, minisamp=10, precise=2, fitfunc='lg', rand_state=123):
        self.maxdepth = depth
        self.minisamp = minisamp
        self.precise = precise
        self.rand_state = rand_state
        if fitfunc == 'lg':
            self.fitfunc = self._newton
        elif fitfunc == 'mean':
            self.fitfunc = self._mean

    def fit(self, x, y):
        self.tree = {}
        self.fity = y.copy()
        yidx = np.arange(len(y))
        self._Splits(x, y, yidx, '0')
        return self, self.fity

    def _mean(self, y):
        return round(np.mean(y), self.precise)

    def _newton(self, y):
        return round(np.sum(y) / np.sum(np.abs(y) * (2 - np.abs(y))), self.precise)

    def _Splits(self, x, y, yidx, code):
        if len(code) > self.maxdepth or len(np.unique(y)) == 1 or len(y) < self.minisamp:
            tmp = self.fitfunc(y)
            self.fity[yidx] = tmp
            self.tree[code] = (False, tmp)
            return self
        fidx = np.random.choice(x.shape[1], 1)[0]
        ks, bstsplts = self._split(x.T[fidx], y)
        self.tree[code] = (True, fidx, bstsplts)
        leftidx = x.T[fidx] <= bstsplts
        rightidx = x.T[fidx] > bstsplts
        self._Splits(x[leftidx], y[leftidx], yidx[leftidx], code + '0')
        self._Splits(x[rightidx], y[rightidx], yidx[rightidx], code + '1')

    # def _ranksplit(self, x, y):
    #     return np.argmax(np.abs(x.T.dot(y)))

    def predict(self, X):
        l = len(X)
        self.predy = np.repeat(0.0, l)
        yidx = np.arange(l)
        self._predict(X, yidx, '0')
        return self.predy

    def _predict(self, x, yidx, code):
        if not self.tree[code][0]:
            self.predy[yidx] = self.tree[code][1]
            return self
        fidx, splts = self.tree[code][1], self.tree[code][2]
        leftidx = x.T[fidx] <= splts
        rightidx = x.T[fidx] > splts
        self._predict(x[leftidx], yidx[leftidx], code + '0')
        self._predict(x[rightidx], yidx[rightidx], code + '1')

    def _split(self, prob, target):
        idx = prob.argsort()
        prob = prob[idx]
        postarget = target[idx]
        ks = np.abs(np.cumsum(postarget))
        midx = np.argmax(ks)
        return ks[midx], prob[midx]