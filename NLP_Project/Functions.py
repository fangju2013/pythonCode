# -*- coding: utf-8 -*-

import numpy as np

punc=[u';',u'；',u':',u'：',u'.',u'。',u',',u'，',u'?',u'？',u'!',u'！',u' ',u'  ',u'    ']
csvdir='C:\\Users\\Administrator\\Desktop\\data_processing\\rawdata\\rawdata0820.csv'
dfsavedir='C:\\Users\\Administrator\\Desktop\\data_processing\\process_data\\df0824.csv'

def tmpfunc(x,a):
    if x in a:
        return 1
    else:
        return 0

def word_pair(w_l,flag='',tg=['v','n','r']):
    pairs=[]
    pairs3=[]
    nw=[]
    for w,t in w_l[:]:
        w_l.pop(0)
        if t in tg:
            nw.append(w)
            if len(w_l)>0 and w_l[0][1] in tg and w_l[0][1]!=t:
                pairs.append(w+w_l[0][0])
                if len(w_l)>1 and w_l[1][1] in tg and w_l[0][1]!=w_l[1][1]:
                    pairs3.append(w+w_l[0][0]+w_l[1][0])
                elif len(w_l)>2 and w_l[2][1] in tg and w_l[0][1]!=w_l[2][1]:
                    pairs3.append(w+w_l[0][0]+w_l[2][0])
            elif len(w_l)>1 and w_l[1][1] in tg[:-1] and w_l[1][1]!=t:
                pairs.append(w+w_l[1][0])
                if len(w_l)>2 and w_l[2][1] in tg and w_l[1][1]!=w_l[2][1]:
                    pairs3.append(w+w[1][0]+w_l[2][0])
                elif len(w_l)>3 and w_l[3][1] in tg and w_l[1][1]!=w_l[3][1]:
                    pairs3.append(w+w_l[1][0]+w_l[3][0])
        else:
            next
    return list(set([flag+i for i in pairs3+pairs+nw]))

def tfidf_trans(ldf):
    weight=[]
    for var in ldf.columns:
        weight.append(len(np.where(ldf[var]!=0)[0]))
    ldf=ldf*weight
    return ldf

def word_imp_qus(w_l,imp_l=[u'才能',u'还能'],qus_l=[u'为什么',u'能不能']):
    for w,t in w_l:
        if w in imp_l:
            return 'imp_'
        elif w in qus_l:
            return 'qus_'
    return 'no'






