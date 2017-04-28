# -*- coding: utf-8 -*-

from __future__ import division
from Huffman import HuffManCode,getMaxCodeLen,getCodeList
from corpus import getWordFreq
import numpy as np



# class word2vec:
#     def __init__(self,wordLen = 100,lr = 0.01,maxIter = 500,wordWin = 2,l2 = 0.01,wordDict = wordDict):
#         self.wordLen = wordLen
#         self.lr = lr
#         self.maxIter = maxIter
#         self.wordWin = wordWin
#         self.l2 = l2
#         self.wordDict = wordDict
#         self.maxCodeLen = getMaxCodeLen(wordDict)
#         self.W = np.random.uniform(0,1,size=(self.wordLen, self.maxCodeLen))
#         self._initWordValue()
#
#     def _initWordValue(self):
#         wordList = self.wordDict.keys()
#         self.X = {}
#         for word in wordList:
#             self.X[word] = np.random.uniform(0,0.1,size=self.wordLen)
#
#     def _sigmoid(self,x):
#         return 1/(1+np.exp(-x))
#
#     def _siggrad(self,x):
#         return (1-self._sigmoid(x))*self._sigmoid(x)
#
#     def _getContX(self,contextWord):
#         contSumX = np.zeros(shape=(1,self.wordLen))
#         for word in contextWord:
#             contSumX[0] += self.X[word]
#         return contSumX
#
#     def _getSentContext(self,sent):
#         for i in range(len(sent)):
#             li = i-self.wordLen
#             lo = i+self.wordLen
#             if li<0:
#                 li=0
#             if lo>len(sent):
#                 lo=len(sent)
#             targetWord = sent[i]
#             contextWord = sent[li:i]+sent[(i+1):(lo+1)]
#             self._fit(targetWord,contextWord)
#
#     def _farbackP(self,targetWord,contextWord):
#         targetWordCodetmp = HuffManCode(self.wordDict)[targetWord]
#         targetWordCode = getCodeList(targetWordCodetmp)
#         contextWordSum = self._getContX(contextWord)
#         a = np.dot(contextWordSum,self.W[:,:len(targetWordCode)])
#         z = self._sigmoid(a)
#         error = (z - targetWordCode) * self._siggrad(a)
#         print a
#         if np.mean(np.abs(error))>0.01:
#             print np.mean(np.abs(error)),error.shape
#         deltaW = np.outer(contextWordSum, error)
#         # error = np.array(error)
#         deltaX = error.dot(self.W[:,:len(targetWordCode)].T)
#         return deltaW,deltaX
#
#     def _fit(self,targetWord,contextWord):
#         targetWordCodeTmp = HuffManCode(self.wordDict)[targetWord]
#         targetWordCode = getCodeList(targetWordCodeTmp)
#         for i in range(self.maxIter):
#             deltaW,deltaX = self._farbackP(targetWord,contextWord)
#             self.W[:,:len(targetWordCode)] -= self.lr*deltaW
#             for word in contextWord:
#                 self.X[word] -= self.lr*deltaX/4
#
#     def train(self,corps):
#         for sent in corps:
#             self._getSentContext(sent)
#         return self.X
#
#     def getMostSimilarWord(self,word,n=10):
#         wordVec = self.X[word]
#         wordList = self.wordDict.keys()
#         simDict={}
#         for wd in wordList:
#             if wd != word:
#                 simDict[wd] = np.sqrt(sum((wordVec-self.X[wd])**2))
#         simList=sorted(simDict.iteritems(),key=lambda d:d[1],reverse=True)
#         return simList[:n]
#
#
# ##############################################################################################
# bb = word2vec(wordLen = 50,lr = 0.01,maxIter = 100,wordWin = 2,wordDict = wordDict)
# bb.train(corps)
# print bb.getMostSimilarWord('dog',n=5)
##############################################################################################
class w2v:
    def __init__(self,lr,wl,hc,huffdepth,wordWin,wordDict,l2):
        self.lr = lr
        self.wl = wl
        self.hc = hc
        self.huffdepth = huffdepth
        self.wordWin = wordWin
        self.wordDict = wordDict
        self.l2 = l2
        self.wv = {}
        for w in wordDict.keys():
            self.wv[w] = np.random.uniform(size = (1,self.wl))
        self.w = np.random.uniform(size = (self.wl,self.huffdepth))
        self.b = np.random.uniform(size = (1,self.huffdepth))

    def fit(self,corps):
        for corp in corps:
            self._fit2(corp)

    def _fit2(self,corp):
        for idx in range(len(corp)):
            w,context = self._getContext(corp,idx)
            self._fit3(w,context)

    def _getContext(self,corp,idx):
        w = corp[idx]
        li = idx - self.wordWin
        lo = idx + self.wordWin
        if li < 0:
            li = 0
        if lo > len(corp):
            lo = len(corp)
        context = corp[li:idx] + corp[(idx+1):(lo+1)]
        return w,context

    def _fit3(self,w,context):
        y = self.hc[w]
        x = self._getx(context)
        deltax,deltaw,deltab = self._back(x,y)
        self.w -= (self.lr*deltaw+self.l2*self.w)
        self.b -= (self.lr*deltab+self.l2*self.b)
        for cw in context:
            self.wv[cw] -= (self.lr*deltax/len(context)+self.l2*self.wv[cw])

    def _back(self,x,y):
        a,z = self._forw(x)
        l = len(y)
        error = np.zeros(shape=(1,self.huffdepth))
        error[0][:l] += (z[0][:l]-y)
        error *=self._siggrad(a)
        print np.mean(abs(error))
        deltax = error.dot(self.w.T)
        deltaw = x.T.dot(error)
        deltab = error
        return deltax,deltaw,deltab

    def _forw(self,x):
        a = x.dot(self.w) + self.b
        z = self._sigmoid(a)
        return a,z

    def _getx(self,context):
        x = np.zeros(shape = (1,self.wl))
        for w in context:
            x += self.wv[w]
        return x

    def _sigmoid(self,x):
        return 1 / (1+np.exp(-x))

    def _siggrad(self,x):
        return (1-self._sigmoid(x)) * (self._sigmoid(x))

    def getMostSimilarWord(self,word,n=10):
        wordVec = self.wv[word]
        wordList = self.wordDict.keys()
        simDict = {}
        for wd in wordList:
            if wd != word:
                simDict[wd] = np.sqrt(np.sum(np.power((wordVec-self.wv[wd]),2)))
        simList = sorted(simDict.iteritems(),key = lambda d:d[1],reverse = False)
        return simList[:n]

#####################################################################
# corps = [['the','as','is','dog','in','a','bedroom'],['the','as','is','cat','in','a','bedroom']]
from nltk.corpus import brown
corps = brown.sents(categories=['news', 'editorial', 'reviews'])
corps = list(corps)
wordDict = getWordFreq(corps)
tmp = HuffManCode(wordDict)
hc = {}
for w in tmp.keys():
    hc[w] = getCodeList(tmp[w])
huffdepth = getMaxCodeLen(wordDict)

wc = w2v(lr=0.001,wl=100,hc=hc,huffdepth=huffdepth,wordWin=3,wordDict=wordDict,l2=0.001)
for i in range(100):
    wc.fit(corps)
print wc.getMostSimilarWord('was',n=5)