# -*- coding: utf-8 -*-

import numpy as np
from collections import Counter

def getSPMap():
    with open("classNames.txt")  as f:
        classNames=f.read().decode('utf-8').strip().split('\n')
    length=len(classNames)
    primaryTitles=[classNames[i]  for i in  range(0,length,2)]
    secondaryTitles=[classNames[i].split('\t')  for i in  range(1,length,2)]
    PrimiaryClass=[]           #得到二级标题和一级标题的元组构成的列表
    second2Pri=[PrimiaryClass.extend(zip(y,[x]*len(y)))for x,y in zip(primaryTitles,secondaryTitles)]
    return dict(PrimiaryClass)   #得到二级标题和一级标题构成的键值对

def getS2P(secondary_list):
    second2Pri=getSPMap()
    PriClass=map(lambda x:second2Pri[x],secondary_list)
    uniqueClass=np.unique(PriClass)  #返回的是array
    ClassCodes=dict(zip(uniqueClass,range(len(uniqueClass))))    #将一级标题进行数字化，得到其键值对
    CodedClass=np.array(map(lambda x:ClassCodes[x],PriClass))
    return CodedClass        #将一级标题转化为对应的数字

def getMostCommon(list_like):
    listCount=Counter(list_like)
    return listCount.most_common(1)[0][0]    #most_common返回元组列表

def findCoOccue(list_like):
    betaMost=len(list_like)*0.8
    betaLess=int(len(list_like)*0.2)
    CoOccue=Counter(list_like)
    if None in CoOccue:
        CoOccue.pop(None)
    MostCoOccue=[]
    LessCoOccue=[]
    for item,freq in CoOccue.iteritems():    #iteritems返回的是字典的迭代器
        if freq>betaMost:
            MostCoOccue.append(item)
        elif freq < betaLess:
            LessCoOccue.append(item)
    return MostCoOccue,LessCoOccue
