# -*- coding: utf-8 -*-

eps = 0.01
import numpy as np
class SACT():
    def __init__(self):
        pass
    def sigmoid(self,x):
        act = 1/(1+np.exp(-x))
        return act,act*(1-act)+eps
    def tanh(self,x):
        act = np.tanh(x)
        return act,(1-act**2)+eps
    def relu(self,x):
        """Compute Rectified Linear Units values for each sets of scores in x."""
        act = x
        actg = x.copy()
        act[act<0]=0
        actg[actg<=0]= 0
        actg[actg>0] = 1
        return act,actg+eps
    def softmax(self,x):
        """Compute softmax values for each sets of scores in x."""
        e_x = np.exp(x)
        act = e_x /np.sum(e_x,axis=1).reshape(x.shape[0],1)
        return act,1
    def sigRelu(self,x):
        act = x.astype('f')
        grad = x.astype('f')
        act[x>0],grad[x>0] = self.sigmoid(x[x>0])
        act[x<=0],grad[x<=0] = 0.5,0
        return act,grad+eps
    def noAct(self,x):
        return x,1
    def getActFunc(self,types):
        if types=='sigmoid':
            return self.sigmoid
        elif types=='tanh':
            return self.tanh
        elif types=='relu':
            return self.relu
        elif types=='softmax':
            return self.softmax
        elif types=='sigrelu':
            return self.sigRelu
        elif types=='noact':
            return self.noAct
actfuncs = SACT()
a = np.random.uniform(size = 100).reshape(20,5)
print actfuncs.softmax(a)
