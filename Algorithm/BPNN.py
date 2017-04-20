# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import time

class BPNN:
    def __init__(self,ni,nh,no,lr,maxIter,l2):
        self.ni = ni
        self.nh = nh
        self.no = no
        self.lr = lr
        self.maxIter = maxIter
        self.l2 = l2
        self.W = np.random.uniform(size=(self.ni, self.nh))
        self.ib = np.random.uniform(size=self.nh)
        self.V = np.random.uniform(size=self.nh)
        self.ob = np.random.uniform(size=self.no)

    def _sigmiod(self,x):
        return 1/(1+np.exp(-x))

    def _siggrad(self,x):
        return (1-self._sigmiod(x))*self._sigmiod(x)

    def _relu(self, x):
        x[x < 0] = 0
        return x

    def _relugrad(self, x):
        x[x <= 0] = 0
        x[x > 0] = 1
        return x

    def _farwardPropagate(self,X):
        a0 = np.dot(X,self.W)+self.ib
        z0 = self._sigmiod(a0)
        a1 = np.dot(z0,self.V)+self.ob
        z1 = self._sigmiod(a1)
        return z1,a1,z0,a0

    def _backwardPropagate(self,X,Y):
        z1,a1,z0,a0 = self._farwardPropagate(X)
        error = (z1-Y)*self._siggrad(a1)
        deltaV = np.dot(error,z0)
        deltaob = np.sum(error)
        deltatmp = np.outer(error,self.V)*self._siggrad(a0)
        deltaW = np.dot(X.T,deltatmp)
        deltaib = np.sum(deltatmp,axis=0)
        return deltaW,deltaib,deltaV,deltaob

    def fit(self,X,Y):
        for i in range(self.maxIter):
            deltaW,deltaib,deltaV,deltaob=self._backwardPropagate(X,Y)
            self.W-=(self.lr*deltaW+self.l2*self.W)
            self.ib-=(self.lr*deltaib+self.l2*self.ib)
            self.V-=(self.lr*deltaV+self.l2*self.V)
            self.ob-=(self.lr*deltaob+self.l2*self.ob)

    def predict(self,X,Y):
        return self._farwardPropagate(X)[0]

#####################################################################
# from sklearn import datasets
# from sklearn.metrics import roc_auc_score
# iris=datasets.load_boston()
# X=iris.data
# X=(X-np.mean(X,axis=0))/np.std(X,axis=0)
# Y=iris.target
# U=np.mean(Y)
# Y[Y<=U]=0
# Y[Y>U]=1
# bb=BPNN(ni=13,nh=25,no=1,lr=0.05,maxIter=10000,l2=0.005)
# bb.fit(X,Y)
# preds=bb.predict(X,Y)
# print roc_auc_score(Y,preds)

########################################################
from sklearn.metrics import roc_auc_score
from sklearn.datasets import make_hastie_10_2
X, y = make_hastie_10_2(random_state=0)
y[y==-1]=0
X_train, X_test = X[:2000], X[2000:]
y_train, y_test = y[:2000], y[2000:]

bb=BPNN(ni=10,nh=20,no=1,lr=0.01,maxIter=10000,l2=0.001)
a=time.time()
bb.fit(X_train,y_train)
preds=bb.predict(X_test,y_test)
b=time.time()
print roc_auc_score(y_test,preds)
print b-a