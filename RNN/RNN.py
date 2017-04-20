# -*- coding: utf-8 -*-

from __future__ import division
from Huffman import getMaxCodeLen, getWordCodeDict
from Corpus import getWordFreq
import numpy as np

corps = [['the', 'as', 'is', 'dog', 'in', 'a', 'bedroom'], ['the', 'as', 'is', 'cat', 'in', 'a', 'bedroom']]
wordDict = getWordFreq(corps)

class BPTT:
    def __init__(self,lr ,wl ,hn ,bt ,n ,l2 ,huffdepth ,wordDict):
        self.lr = lr
        self.wl = wl
        self.hn = hn
        self.bt = bt
        self.n = n
        self.l2 = l2
        self.huffdepth = huffdepth
        self.wordDict = wordDict

        self.U = np.random.uniform(-1/np.sqrt(self.n),1/np.sqrt(self.n),size=(self.hn,self.wl))
        self.V = np.random.uniform(-1/np.sqrt(self.n),1/np.sqrt(self.n),size=(self.huffdepth,self.hn))
        self.W = np.random.uniform(-1/np.sqrt(self.n),1/np.sqrt(self.n),size=(self.hn,self.hn))

        self.wv = {}
        for w in self.wordDict.keys():
            self.wv[w] = np.random.uniform(size = self.wl)

    def _sigmoid(self,x):
        return 1/(1+np.exp(-x))

    def _siggrad(self,x):
        return (1-self._sigmoid(x))*self._sigmoid(x)

    def _forwardP(self,corp):
        T = len(corp)
        z = np.zeros((T-1, self.hn))
        s = np.zeros((T,self.hn))
        a = np.zeros((T-1,self.huffdepth))
        o = np.zeros((T-1,self.huffdepth))
        for t in np.arange(T-1):
            z[t] = self.U.dot(self.wv[corp[t]])+self.W.dot(s[t-1])
            s[t] = np.tanh(z[t])
            a[t] = self.V.dot(s[t])
            o[t] = self._sigmoid(a[t])
        return o,a,s,z

    def _backwardP(self,corp):
        T = len(corp)
        Y = self._getY(corp)
        o,a,s,z = self._forwardP(corp)
        dLdU = np.zeros(self.U.shape)
        dLdV = np.zeros(self.V.shape)
        dLdW = np.zeros(self.W.shape)
        dLdX = np.zeros((T-1,self.wl))
        error = (o - Y)*self._siggrad(a)
        for t in np.arange(T-1)[::-1]:
            dLdV += np.outer(error[t],s[t])
            delta_t = self.V.T.dot(error[t])*(1-np.power(np.tanh(s[t]),2))
            print delta_t[:4]
            dLdX[t] = self.U.T.dot(delta_t)
            for bt in np.arange(max(0,t-self.bt),t+1)[::-1]:
                dLdW += np.outer(delta_t,s[bt-1])
                dLdU += np.outer(delta_t,self.wv[corp[t]])
                delta_t = self.W.T.dot(delta_t)*(1-np.power(np.tanh(s[bt-1]),2))
        return dLdU,dLdV,dLdW,dLdX

    def _getY(self,corp):
        T = len(corp)
        hc = getWordCodeDict(self.wordDict)
        Y = []
        for i in range(1,T):
            tmp = hc[corp[i]]
            if len(tmp) < self.huffdepth:
                Y.append(tmp + [0]*(self.huffdepth - len(tmp)))
            else:
                Y.append(tmp)
        return np.array(Y)

    def fit(self,corps):
        for corp in corps:
            self._fit2(corp)

    def _fit2(self,corp):
        T = len(corp)
        dLdU,dLdV,dLdW,dLdX = self._backwardP(corp)
        self.U -= (self.lr*dLdU + self.l2*self.U)
        self.V -= (self.lr*dLdV + self.l2*self.V)
        self.W -= (self.lr*dLdW + self.l2*self.W)
        for t in np.arange(T-1)[::-1]:
            self.wv[corp[t]] -= (self.lr*dLdX[t]+self.l2*self.wv[corp[t]])

    def getMostSimilarWord(self,word,n=10):
        wordVec = self.wv[word]
        wordList = self.wordDict.keys()
        simDict = {}
        for wd in wordList:
            if wd != word:
                simDict[wd] = np.sqrt(np.sum(np.power((wordVec-self.wv[wd]),2)))
        simList = sorted(simDict.iteritems(),key = lambda d:d[1],reverse = False)
        return simList[:n]

#######################################################################################
corps = [['the','as','is','dog','in','a','bedroom'],['the','as','is','cat','in','a','bedroom']]
wordDict = getWordFreq(corps)
huffdepth = getMaxCodeLen(wordDict)
rnn = BPTT(lr=0.005,wl=100,hn=100,bt=4,n=5000,l2=0.005,huffdepth=huffdepth,wordDict=wordDict)
for i in range(1000):
    rnn.fit(corps)
print rnn.getMostSimilarWord('cat',n=5)
