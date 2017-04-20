# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import jieba
import jieba.posseg as pseg
from collections import Counter
import lda
import matplotlib.pyplot as plt
import cPickle
import sys
reload(sys)
sys.setdefaultencoding('utf8')

dirLeft = u'E:\\Project\\文本聚类\\details\\11m\\s ('
wtb = pd.DataFrame(columns = [u'记录时间',u'会话Id', u'消息来源', u'消息目标', u'消息内容'])
for i in range(1,40):
    rawdata = pd.read_csv(dirLeft+str(i)+u').csv',header=0,encoding='gbk')
    wtb = pd.concat([wtb, rawdata])
    wtb =  wtb.loc[wtb[u'消息目标'] == u'机器人',:]
    wtb = wtb.sort([u'会话Id'])
    wtb = wtb.reset_index()
    del wtb['index']

def getMainDict(maindata):
    mainDict = {}
    for i in np.arange(0,maindata.shape[0]):
        mainDict.setdefault(maindata[u'会话Id'][i],[])
        mainDict[maindata[u'会话Id'][i]].append(maindata[u'消息内容'][i])
    return mainDict

def getMainCutDict(mainDict):
    mainCutDict = {}
    for key in mainDict.keys():
        mainCutDict[key] = [jieba.lcut(line,cut_all = False) for line in mainDict[key] if len(str(line)) > 6]
    return mainCutDict

# def getMainCutDict(mainDict):
#     mainCutDict = {}
#     for key in mainDict.keys():
#         tmp = mainDict[key]
#         tmpList = [pseg.lcut(line) for line in tmp if len(str(line)) > 6]
#         tmp1 = []
#         for line in tmpList:
#             tmp2 = []
#             for w in line:
#                 if w.flag in ('v','n','ns','vs','nv'):
#                     tmp2.append(w.word)
#             tmp1.append(tmp2)
#         mainCutDict[key] = tmp1
#     return mainCutDict

mainDict = getMainDict(wtb)
mainCutDict = getMainCutDict(mainDict)
cPickle.dump(mainCutDict,open("D:\\GetKeyWord\\pick.pkl","wb"))

# get the pickle file
pkl_file = open("D:\\GetKeyWord\\pick.pkl","rb")
mainCutDict = cPickle.load(pkl_file)
pkl_file.close()

def getMergeDict(mainCutDict):
    mergeDict = {}
    for key in mainCutDict.keys():
        for line in mainCutDict[key]:
            mergeDict.setdefault(key,[])
            mergeDict[key].extend(line)
    return mergeDict

def getUniqueMergeDict(mergeDict):
    uniqueMergeDict = {}
    for key in mergeDict.keys():
        uniqueMergeDict[key] = list(set(mergeDict[key]))
    return uniqueMergeDict

def getWordFreqDict(mergeDict):
    wordList = []
    for key in mergeDict.keys():
        wordList.extend(mergeDict[key])
    wordFreqDict = dict(Counter(wordList))
    return wordFreqDict

def getIdDict(mergeDict):
    idDict = {}
    i = 0
    for key in mergeDict.keys():
        idDict[key] = i
        i = i+1
    return idDict

def getWordList(mergeDict):
    wordList = []
    for key in mergeDict.keys():
        wordList.extend(mergeDict[key])
    wordList = list(set(wordList))
    return wordList

def getWordDict(wordList):
    wordDict = {}
    i = 0
    for word in wordList:
        wordDict[word] = i
        i = i + 1
    return wordDict

def getWordMatrix(idDict,wordDict,uniqueMergeDict,wordFreqDict):
    wordMat = np.zeros((len(idDict),len(wordDict)),dtype='int32')
    for id in uniqueMergeDict.keys():
        tmpWord = uniqueMergeDict[id]
        for word in tmpWord:
            wordMat[idDict[id]][wordDict[word]] = wordFreqDict[word]
    return wordMat

######################################
mergeDict = getMergeDict(mainCutDict)
uniqueMergeDict = getUniqueMergeDict(mergeDict)
wordFreqDict = getWordFreqDict(mergeDict)
idDict = getIdDict(mergeDict)
wordList = getWordList(mergeDict)
wordDict = getWordDict(wordList)
wordMat = getWordMatrix(idDict,wordDict,uniqueMergeDict,wordFreqDict)
print wordMat.shape
###################################################################
model = lda.LDA(n_topics = 10, n_iter = 150, random_state = 1)
model.fit(wordMat)
topic_word = model.topic_word_
n_topic_word = 8
for i,topic_dict in enumerate(topic_word):
    topic_words = np.array(wordList)[np.argsort(topic_dict)][:-n_topic_word:-1]
    print 'Topic {}:{}'.format(i,' '.join(topic_words))