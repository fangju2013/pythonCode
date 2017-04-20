# -*- coding: utf-8 -*-

import numpy as np
import random
from sklearn import datasets
from sklearn.metrics import roc_auc_score

class LogRegs:
    def __init__(self,alpha=0.01,maxIter=500):
        self.alpha=alpha
        self.maxIter=maxIter

    def _sigmoid(self,x):
        return 1.0/(1+np.exp(-x))

    def trainLogRegs(self,X,Y):
        X_sample,X_feature=X.shape       #np.shape(X)
        weights=np.random.uniform(0,size=X_feature)

        for k in range(self.maxIter):
            # if self.opts=='GradAscent':
            output=self._sigmoid(np.dot(X,weights))
            error=Y-output
            weights=weights+self.alpha*np.dot(X.T,error)

            # elif self.opts=='stocGradAscent':
            #     for j in range()
            #     for i in range(X_sample):
            #         output=self._sigmoid(np.dot(X[i],weights))
            #         error=Y[i,]-output
            #         weights=weights+self.alpha*X[i]*error
            #
            # elif self.opts=='smoothStocGradAscent':
            #     dataIndex=range(X_sample)
            #     for i in range(X_sample):
            #         alpha=0.5/(1.0+k+i)+0.01
            #         randIndex=int(random.uniform(0,len(dataIndex)))
            #         output=self._sigmoid(np.dot(X[randIndex,:],weights))
            #         error=Y[randIndex,]-output
            #         weights=weights+self.alpha*X[randIndex,:].reshape((len(X[randIndex,]),1))*error
            #         del dataIndex[randIndex]
            # else:
            #     raise NameError('Not suppot optimize method type!')

        return weights

    def testLogRegs(self,weights,test_X,test_Y):
        X_sample,X_feature=np.shape(test_X)
        count=1
        for i in xrange(X_sample):
            predict=self._sigmoid(np.dot(test_X[i,],weights))[0]>0.5
            if predict == bool(test_Y[i,]):
                count+=1
        accuracy=float(count)/X_sample
        return accuracy

    def pred(self,weights,X):
        prob=self._sigmoid(np.dot(X,weights))
        return prob

######################################
iris = datasets.load_boston()
X = iris.data
Y = iris.target
u = np.mean(Y)
Y[Y <= u] = 0
Y[Y > u] = 1

Log=LogRegs(alpha=0.001,maxIter=100000)
weights=Log.trainLogRegs(X,Y)
ypred=Log.pred(weights,X)
print roc_auc_score(Y,ypred)