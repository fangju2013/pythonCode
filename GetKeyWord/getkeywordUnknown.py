# -*- coding: utf-8 -*-

from __future__ import division
import csv
import jieba
import jieba.posseg as pseg
import pandas as pd
import numpy as np
from collections import Counter
import cPickle
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

Left = u'E:\\MSXF\\客服关键词提取\\unknowns\\unknow\\'
tb = pd.DataFrame(columns = [u'会话Id',u'未知问题',u'创建时间',u'类型'])
for i in range(1,3):
    rawdata = pd.read_csv(Left+str(i)+u'.csv',header=0,encoding='gbk')
    tb = pd.concat([tb,rawdata])
    tb = tb.sort([u'会话Id'])
    tb = tb.reset_index()
    del tb['index']
print tb

# def getMainDict(maindata):
#     mainDict = {}
#     for i in np.arange(0,maindata.shape[0]):
#         mainDict.setdefault(maindata[u'会话Id'][i],[])
#         mainDict[maindata[u'会话Id'][i]].append(maindata[u'消息内容'][i])
#     return mainDict

def getMainDict(maindata):
    mainDict = {}
    for i in np.arange(0,maindata.shape[0]):
        mainDict.setdefault(maindata[u'会话Id'][i],[])
        mainDict[maindata[u'会话Id'][i]].append(maindata[u'未知问题'][i])
    return mainDict

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

# mainDict = getMainDict(wtb)
# mainCutDict = getMainCutDict(mainDict)
# cPickle.dump(mainCutDict,open("D:\\GetKeyWord\\pick.pkl","wb"))

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
mainDict = getMainDict(tb)
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
# print tfidfDict
# csvfile = file(u'E:\\MSXF\\客服关键词提取\\unknown\\keyword2.csv','wb')
# writer = csv.writer(csvfile)
# writer.writerows(mostImportWord)
# csvfile.close()


