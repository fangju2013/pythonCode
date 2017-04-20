# -*- coding: utf-8 -*-
"""multiple perceptron"""

from __future__ import division
import numpy as np
import random
import time

class MLP:
    def __init__(self):
        self.ni=0
        self.nh=0
        self.no=0
        self.input_cells=[]
        self.hidden_cells=[]
        self.output_cells=[]
        self.input_weights=[]
        self.output_weights=[]
        self.input_correction=[]
        self.output_correction=[]

    def _sigmoid(self,x):
        return 1/(1+np.exp(-x))

    def _sigmoidDev(self,x):
        return np.exp(-x)/((1+np.exp(-x))**2)

    def _getRandom(self,a,b):
        return (b-a)*random.random()+a

    def _makeMat(self,m,n,fill=0):
        mat=[]
        for i in range(m):
            mat.append([fill]*n)
        return mat

    def setInitValue(self,ni,nh,no):
        self.ni=ni+1
        self.nh=nh
        self.no=no
        self.input_cells=[1]*self.ni
        self.hidden_cells=[1]*self.nh
        self.output_cells=[1]*self.no
        self.input_weights=self._makeMat(self.ni,self.nh)
        self.output_weights=self._makeMat(self.nh,self.no)
        for i in range(self.ni):
            for h in range(self.nh):
                self.input_weights[i][h]=self._getRandom(-1.0,1.0)
        for h in range(self.nh):
            for o in range(self.no):
                self.output_weights[h][o]=self._getRandom(-1.0,1.0)
        self.input_correction=self._makeMat(self.ni,self.nh)
        self.output_correction=self._makeMat(self.nh,self.no)

    def forwardPropagate(self,input):
        for i in range(self.ni-1):
            self.input_cells[i]=input[i]
        for j in range(self.nh):
            for j in range(self.nh):
                total = 0
                for i in range(self.ni):
                    total += self.input_cells[i] * self.input_weights[i][j]
                self.hidden_cells[j] = self._sigmoid(total)
            for k in range(self.no):
                total = 0
                for j in range(self.nh):
                    total += self.hidden_cells[j] * self.output_weights[j][k]
                self.output_cells[k] = self._sigmoid(total)
            return self.output_cells[:]

        def backwardPropagate(self, sample, label, lr, alpha):
            self.forwardPropagate(sample)
            output_delta = [0.0] * self.no
            for o in range(self.no):
                error = label[o] - self.output_cells[o]
                output_delta[o] = self._sigmoidDev(self.output_cells[o]) * error
            hidden_delta = [0.0] * self.nh
            for h in range(self.nh):
                error = 0.0
                for o in range(self.no):
                    error += output_delta[o] * self.output_weights[h][o]
                hidden_delta[h] = self._sigmoidDev(self.hidden_cells[h]) * error
            for h in range(self.nh):
                for o in range(self.no):
                    change = output_delta[o] * self.hidden_cells[h]
                    self.output_weights[h][o] += lr * change + alpha * self.output_correction[h][o]
                    self.output_correction[h][o] = change
            for i in range(self.ni):
                for h in range(self.nh):
                    change = hidden_delta[h] * self.input_cells[i]
                    self.input_weights[i][h] += lr * change + alpha * self.input_correction[i][h]
                    self.input_correction[i][h] = change
            error = 0.0
            for o in range(len(label)):
                error += 0.5 * (label[o] - self.output_cells[o]) ** 2
            return error

        def train(self, samples, labels, maxIter=10000, lr=0.01, alpha=0.1):
            for i in range(maxIter):
                error = 0
                for i in range(len(samples)):
                    sample = samples[i]
                    label = labels[i]
                    error += self.backwardPropagate(sample, label, lr, alpha)
            return error

#####################################################
samples=[[0,0],[0,1],[1,0],[1,1]]
labels=[[0],[1],[1],[0]]

from sklearn import datasets
from sklearn.metrics import roc_auc_score, roc_curve
# iris = datasets.load_boston()
# samples = iris.data
# labels = iris.target
# U = np.mean(labels)
# labels[labels <= U] = 0
# labels[labels > U] = 1

a = time.time()
nn = MLP()
nn.setInitValue(2, 5, 1)

preds = []
for sample in samples:
    print nn.train(samples, labels, maxIter=1000, lr=0.05, alpha=0.5)
roc_auc_score(labels, preds)
roc_curve(labels, preds)
b = time.time()
print b - a








