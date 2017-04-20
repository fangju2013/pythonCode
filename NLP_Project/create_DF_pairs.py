# -*- coding: utf-8 -*-

import csv
import jieba.posseg as pseg
from Functions import word_pair,tmpfunc,dfsavedir,punc,csvdir
import pandas as pd
import numpy as np

csvfile=file(csvdir,'rb')
rawdata=csv.reader(csvfile)
next(rawdata)

word_list_list=[]
big_word_list=[]
for line in rawdata:
    label=line[1].split('/')
    if len(label)>2:
        label.pop()
    label='/'.join(label)
    line[0]=line[0]+'!'
    cut=pseg.cut(line[0])
    word_list=[]
    w_l=[]
    w_d={}
    idx=1
    for word,tag in cut:
        if len(word)==1:
            tag='nothing'
        if word in punc and len(w_l)>1:
            w_d[idx]=w_l
            idx+=1
            w_l=[]
        else:
            w_l.append((word,tag))
    if len(w_d.keys())>0:
        lidx=w_d.keys()[-1]
        for idx in w_d.keys():
            word_list=word_list+word_pair(w_d[idx])
    big_word_list=big_word_list+word_list
    word_list_list.append((word_list,label,line[0]))

feature=list(set(big_word_list))

data=[]
for w_l,label,raw in word_list_list:
    f=map(lambda x:tmpfunc(x,w_l),feature)      #map函数返回的是list
    f.append(label)
    f.append(raw)
    data.append(tuple(f))
csvfile.close()
for i in ['label','reply']:
    feature.append(i)

df=pd.DataFrame(np.array(data),columns=feature)
df.to_csv(dfsavedir,index=False,encoding='utf8')
