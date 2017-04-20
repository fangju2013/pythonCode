# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np

class TanhLayer:
    def __init__(self, ni, no, lr, l2):
        self.ni = ni
        self.no = no
        self.lr = lr
        self.l2 = l2
        self.W = np.random.uniform(size=(self.ni,self.no))
        self.b = np.random.uniform(size=(1,self.no))

    def forwardP(self,X):
        self.X = X
        self.a = np.dot(self.X, self.W) + self.b
        z = np.tanh(self.a)
        return z

    def fit(self,error):
        error = error * (1-np.power(np.tanh(self.a),2))
        self.W -= (self.lr * self.X.T.dot( error) + self.l2 * self.W)
        self.b -= (self.lr * np.sum(error, axis=0) + self.l2 * self.b)
        error = error.dot(self.W.T)
        return  error

class SigmoidLayer:
    def __init__(self, ni, no, lr, l2):
        self.ni = ni
        self.no = no
        self.lr = lr
        self.l2 = l2
        self.W = np.random.uniform(size=(self.ni, self.no))
        self.b = np.random.uniform(size=(1, self.no))

    def _sigmiod(self, x):
        return 1 / (1 + np.exp(-x))

    def _siggrad(self, x):
        return (1 - self._sigmiod(x)) * self._sigmiod(x)

    def forwardP(self,X):
        self.X = X
        self.a = np.dot(self.X, self.W) + self.b
        z = self._sigmiod(self.a)
        return z

    def fit(self, error):
        error = error * self._siggrad(self.a)
        self.W -= (self.lr * self.X.T.dot(error) + self.l2 * self.W)
        self.b -= (self.lr * np.sum(error, axis=0) + self.l2 * self.b)
        error = error.dot(self.W.T)
        return error

class ReluLayer(SigmoidLayer):
    # def __init__(self,ni,no,lr,l2):
    #     SigmoidLayer.__init__(self,ni,no,lr,l2)

    def _sigmiod(self,x):
        x[x < 0] = 0
        return x

    def _siggrad(self,x):
        x[x <= 0] = 0
        x[x > 0] = 1
        return x

class MultiLayer:
    def __init__(self,ni,nh1,nh2,nh3,lr,l2,maxIter = 1000):
        self.ni = ni
        self.nh1 = nh1
        self.nh2 = nh2
        self.nh3 = nh3
        self.lr = lr
        self.l2 = l2
        self.maxIter = maxIter
        self.h1 = TanhLayer(ni=self.ni,no=self.nh1,lr=self.lr,l2=self.l2)
        self.h2 = ReluLayer(ni=self.nh1,no=self.nh2,lr=self.lr,l2=self.l2)
        self.h3 = SigmoidLayer(ni=self.nh2,no=self.nh3,lr=self.lr,l2=self.l2)

    def fit(self,X,Y):
        for i in range(self.maxIter):
            z1 = self.h1.forwardP(X)
            z2 = self.h2.forwardP(z1)
            z3 = self.h3.forwardP(z2)
            error = z3 - Y
            error1 = self.h3.fit(error)
            error2 = self.h2.fit(error1)
            error3 = self.h1.fit(error2)
            print np.mean(abs(error))

####################################################################################
from sklearn.metrics import roc_auc_score
from sklearn.datasets import make_hastie_10_2
X, y = make_hastie_10_2(random_state=0)
y[y==-1]=0
X_train, X_test = X[:2000], X[2000:]
y_train, y_test = y[:2000], y[2000:]

# print y_train
# nh1 = HiddenLayer(lr=0.05,ni=10,no=50,l2=0.0005)
# nh2 = SigmoidLayer(lr=0.05,ni=50,no=1,l2=0.0005)
# for i in range(1000):
#     z = nh1.forwordP(X_train)
#     z1 = nh2.forwordP(z)
#     error = z1 - y_train.reshape(2000,1)
#     error1 = nh2.fit(error)
#     error2 = nh1.fit(error1)
#     print np.mean(abs(error))
nh = MultiLayer(ni=10,nh1=30,nh2=20,nh3=1,lr=0.005,l2=0.0001,maxIter=2000)
nh.fit(X_train,y_train.reshape(2000,1))
