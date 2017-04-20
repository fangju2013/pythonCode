# -*- coding: utf-8 -*-

from __future__ import division
import csv
import jieba
import jieba.posseg as pseg
import pandas as pd
import numpy as np
from collections import Counter
from sklearn.cluster import KMeans
import cPickle
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

dirLeft = u'E:\\Project\\文本聚类\\details\\11m\\s ('
wtb = pd.DataFrame(columns = [u'记录时间',u'会话Id', u'消息来源', u'消息目标', u'消息内容'])
for i in range(1,20):
    rawdata = pd.read_csv(dirLeft+str(i)+u').csv',header=0,encoding='gbk')
    wtb = pd.concat([wtb, rawdata])
    wtb =  wtb.loc[wtb[u'消息目标'] == u'机器人',:]
    wtb = wtb.sort([u'会话Id'])
    wtb = wtb.reset_index()
    del wtb['index']

# Left = u'E:\\MSXF\\客服关键词提取\\unknowns\\unknow\\'
# tb = pd.DataFrame(columns = [u'会话Id',u'未知问题',u'创建时间',u'类型'])
# for i in range(1,3):
#     rawdata = pd.read_csv(Left+str(i)+u'.csv',header=0,encoding='gbk')
#     tb = pd.concat([tb,rawdata])
#     tb = tb.sort([u'会话Id'])
#     tb = tb.reset_index()
#     del tb['index']


def getMainDict(maindata):
    mainDict = {}
    for i in np.arange(0,maindata.shape[0]):
        mainDict.setdefault(maindata[u'会话Id'][i],[])
        mainDict[maindata[u'会话Id'][i]].append(maindata[u'消息内容'][i])
    return mainDict

# def getMainDict(maindata):
#     mainDict = {}
#     for i in np.arange(0,maindata.shape[0]):
#         mainDict.setdefault(maindata[u'会话Id'][i],[])
#         mainDict[maindata[u'会话Id'][i]].append(maindata[u'未知问题'][i])
#     return mainDict

# def getMainCutDict(mainDict):
#     mainCutDict = {}
#     for key in mainDict.keys():
#         mainCutDict[key] = [jieba.lcut(line,cut_all = False) for line in mainDict[key] if len(str(line)) > 6]
#     return mainCutDict

def getMainCutDict(mainDict):
    mainCutDict = {}
    for key in mainDict.keys():
        tmp = mainDict[key]
        tmpList = [pseg.lcut(line) for line in tmp if len(str(line)) > 6]
        tmp1 = []
        for line in tmpList:
            tmp2 = []
            for w in line:
                if w.flag in ('v','n','ns','vs','nv'):
                    tmp2.append(w.word)
            tmp1.append(tmp2)
        mainCutDict[key] = tmp1
    return mainCutDict

###################################################################################
mainDict = getMainDict(wtb)
mainCutDict = getMainCutDict(mainDict)
cPickle.dump(mainCutDict,open("D:\\GetKeyWord\\pick.pkl","wb"))
pkl_file = open("D:\\GetKeyWord\\pick.pkl","rb")
mainCutDict = cPickle.load(pkl_file)
pkl_file.close()
#################################################################################

def getMergeDict(mainCutDict):
    mergeDict = {}
    for key in mainCutDict.keys():
        for line in mainCutDict[key]:
            mergeDict.setdefault(key,[])
            mergeDict[key].extend(line)
    return mergeDict

def getPersonDict(mergeDict):
    personDict = {}
    for key in mergeDict.keys():
        personDict[key] = len(mergeDict[key])
    return personDict

def getFreqDict(mergeDict):
    freqDict = {}
    for key in mergeDict.keys():
        freqDict[key] = dict(Counter(mergeDict[key]))
    return freqDict

def getTfDict(freqDict,personDict):
    tfDict = {}
    for key in freqDict.keys():
        tmpdict = freqDict[key]
        tmpDict = {}
        for word in tmpdict.keys():
            tmpDict[word] = tmpdict[word] / personDict[key]
        tfDict[key] = tmpDict
    return tfDict

def getIdfWordDict(mergeDict):
    idfWord = []
    for key in mergeDict.keys():
        tmp = np.unique(mergeDict[key])
        idfWord.extend(tmp)
    idfWordDict = dict(Counter(idfWord))
    return idfWordDict

def getIdfDict(tfDict,idfWordDict):
    D = len(tfDict)
    idfDict = {}
    for key in idfWordDict.keys():
        idfDict[key] = np.log(D / idfWordDict[key])
    return idfDict

def getTfidfDict(tfDict,idfDict):
    tfidfDict = {}
    for key in tfDict.keys():
        tmpdict = tfDict[key]
        tmpDict = {}
        for word in tmpdict.keys():
            if word in idfDict.keys():
                tmpDict[word] = tmpdict[word] * idfDict[word]
        tfidfDict[key] = tmpDict
    return tfidfDict

def getSortDict(tfidfDict):
    sortDict = {}
    for key in tfidfDict.keys():
        sortDict[key] = sorted(tfidfDict[key].iteritems(),key = lambda d:d[1],reverse=True)
    return sortDict

def getExtractDict(sortDict):
    extractDict = []
    for key in sortDict.keys():
        extractDict.extend(sortDict[key][0:2])
    return extractDict

def getWordFreq(extractDict):
    wordFreq = []
    for line in extractDict:
        wordFreq.append(line[0])
    return wordFreq

def getWordFreqDict(wordFreq):
    wordFreqDict = dict(Counter(wordFreq))
    wordFreqDict = sorted(wordFreqDict.iteritems(),key = lambda d:d[1],reverse=True)
    return wordFreqDict

def getMostImportWord(wordFreqDict):
    mostImportWord = []
    for line in wordFreqDict[0:200]:
        mostImportWord.append(line)
    return mostImportWord
#####################################################################################################
mainDict = getMainDict(wtb)
mainCutDict = getMainCutDict(mainDict)
mergeDict = getMergeDict(mainCutDict)
personDict = getPersonDict(mergeDict)
freqDict = getFreqDict(mergeDict)
tfDict = getTfDict(freqDict,personDict)
idfWordDict = getIdfWordDict(mergeDict)
idfDict = getIdfDict(tfDict,idfWordDict)
tfidfDict = getTfidfDict(tfDict,idfDict)
sortDict = getSortDict(tfidfDict)
extractDict = getExtractDict(sortDict)
wordFreq = getWordFreq(extractDict)
wordFreqDict = getWordFreqDict(wordFreq)
mostImportWord = getMostImportWord(wordFreqDict)

# csvfile = file(u'E:\\MSXF\\客服关键词提取\\detail\\keyword2.csv','wb')
# writer = csv.writer(csvfile)
# writer.writerows(mostImportWord)
# csvfile.close()

########################################################################################################
# mainDict = getMainDict(tb)
# mainCutDict = getMainCutDict(mainDict)
# mergeDict = getMergeDict(mainCutDict)
# personDict = getPersonDict(mergeDict)
# freqDict = getFreqDict(mergeDict)
# tfDict = getTfDict(freqDict,personDict)
# idfWordDict = getIdfWordDict(mergeDict)
# idfDict = getIdfDict(tfDict,idfWordDict)
# tfidfDict = getTfidfDict(tfDict,idfDict)
# sortDict = getSortDict(tfidfDict)
# extractDict = getExtractDict(sortDict)
# wordFreq = getWordFreq(extractDict)
# wordFreqDict = getWordFreqDict(wordFreq)
# mostImportWord = getMostImportWord(wordFreqDict)
# print tfidfDict
# csvfile = file(u'E:\\MSXF\\客服关键词提取\\unknown\\keyword2.csv','wb')
# writer = csv.writer(csvfile)
# writer.writerows(mostImportWord)
# csvfile.close()
##############################################################################################
# k-means聚类
def getIdDict(tfidfDict):
    idDict = {}
    i = 0
    for key in tfidfDict.keys():
        idDict[key] = i
        i = i+1
    return idDict

def getWordList(tfidfDict):
    wordList = []
    for key in tfidfDict.keys():
        tmpDict = tfidfDict[key]
        wordList.extend(tmpDict.keys())
    wordList = list(set(wordList))
    return wordList

def getWordDict(wordList):
    wordDict = {}
    i = 0
    for word in wordList:
        wordDict[word] = i
        i = i+1
    return wordDict

def getIdWordMat(idDict,wordDict):
    IdWordMat = np.zeros((len(idDict),len(wordDict)))
    for id in tfidfDict.keys():
        tmpDict = tfidfDict[id]
        for word in tmpDict.keys():
            IdWordMat[idDict[id]][wordDict[word]] = tmpDict[word]
    return IdWordMat

idDict = getIdDict(tfidfDict)
wordList = getWordList(tfidfDict)
wordDict = getWordDict(wordList)
IdWordMat = getIdWordMat(idDict,wordDict)
kmeans = KMeans(n_clusters=10,random_state=0).fit(IdWordMat.T)
labels = kmeans.labels_
result = []
for i in range(10):
    class1 =  np.where(labels == i)[0]
    classWord = []
    for word in wordDict.keys():
        if wordDict[word] in class1:
            classWord.append(word)

    wordClass = []
    for line in mostImportWord:
        if line[0] in classWord:
            wordClass.append(line)
    lineWord = []
    for line in wordClass[0:10]:
        lineWord.append(line[0])
    result.append(lineWord)

for line in result:
    tmp = line
    print '/'
    for word in tmp:
        print word

