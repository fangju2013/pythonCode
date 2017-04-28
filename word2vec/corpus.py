# -*- coding: utf-8 -*-

import jieba
from collections import Counter
import numpy

def getCorpus():
    sign=['。','！','？','……']
    with open('newcorpus.txt') as f:
        list_doc=f.read()
        for i in sign:
            list_doc=list_doc.replace(i,'$')
        list_doc=list_doc.strip().split('$')
        list_doc_cut=[jieba.lcut(line) for line in list_doc]
    return  list_doc_cut

def getStopWord():
    with open('Ch_stopList.txt') as f:
        list_stop=f.read().decode('utf-8').split('\n')
    return list_stop

def getNewCorpus(list_doc,list_stop):
    new_corpus=[]
    for sent in list_doc:
        tmp=[]
        for word in sent:
            if word not in list_stop:
                tmp.append(word)
        new_corpus.append(tmp)
    return new_corpus

def getWordFreq(list_doc):
    doc_list=[]
    for line in list_doc:
        doc_list.extend(line)
    wordFreq=dict(Counter(doc_list))
    return wordFreq

# list_doc=getCorpus()
# list_stop=getStopWord()
# new_corpus=getNewCorpus(list_doc,list_stop)

