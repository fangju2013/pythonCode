# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from collections import Counter

class df2distdf():
    def __init__(self,X_train,y_train,reply_train):
        self._judge_type(y_train,reply_train)
        self.X_train=X_train
        self.y_train=y_train
        self.reply_train=reply_train
        self.feature=X_train.columns
        self.labels=list(set(self._get_labels(self.y_train)))

    def _judge_type(self,y_train,reply_train):
        if isinstance(y_train,list) and isinstance(reply_train,list):
            next
        else:
            print 'not list type'
            raise StopIteration

    def fit(self,X_test,y_test):
        px,mskpx=self._x2px(X_test)
        py=self._y2py(y_test)
        mask=np.all(np.equal(mskpx,0),axis=1)
        df=pd.DataFrame(px[~mask],columns=self.feature)
        df['plabel']=py[~mask]
        return df

    def fit_x(self,X_test):
        px,mskpx=self._x2px(X_test)
        df=pd.DataFrame(px,columns=self.feature)
        return df

    def get_most_similar_reply(self,X_add,reply,probs,n=5):
        ss=False
        index=list(np.argsort(probs)[:n])
        label=''
        si_idx=[]
        for idx in index:
            print ' '*60+'-----------------------------------------'
            flag=raw_input(' '*60+reply+'\n'+' '*60+self.reply_train[idx]+'\n'*5)
            if flag=='1':
                print 'similar'
                label=label+'#'+self.y_train[idx]
                si_idx.append(idx)
            elif flag=='ss':
                ss=True
                label=label+'#'+self.y_train[idx]
                si_idx.append(idx)
                print 'same sentence'
            else:
                print 'not similar'
        if label=='':
            X_test=X_add
            y_test=[self._get_new_label()]
            self.add_xy(X_test,y_test,[reply])
        else:
            for idx in si_idx:
                self.y_train[idx]=label
            X_test=self.X_train.iloc[si_idx]
            y_test=[label]*len(si_idx)
            if not ss:
                self.add_xy(X_add,[label],[reply])
                X_test=pd.concat([X_test,X_add])
                y_test=y_test+[label]

    def _get_new_label(self):
        nlb='label_%d' % len(self.labels)
        self.labels.append(nlb)
        return nlb

    def add_xy(self,X_test,y_test,reply_test):
        self._judge_type(y_test,reply_test)
        self.X_train=pd.concat([self.X_train,X_test])
        self.y_train=self.y_train+y_test
        self.reply_train=self.reply_train+reply_test

    def add_fit_xy(self,X_test,y_test,reply_test):
        df=self.fit(X_test,y_test)
        self.add_xy(X_test,y_test,reply_test)
        return df

    def _x2px(self,Xte):
        Xtr=np.array(self.X_train)
        Xte=np.array(Xte)
        for i in range(Xte.shape[0]):
            if i==0:
                px=Xtr+Xte[i]
                mskpx=Xtr-Xte[i]
            else:
                px=np.vstack((px,Xtr+Xte[i]))
                mskpx=np.vstack((mskpx,Xtr-Xte[i]))
            px[px==1]=-1
        return px,mskpx

    def _get_label(self,y):
        tmp=y.split('/')
        tmp=Counter(tmp)
        tmp=max(tmp,key=tmp.get)
        return tmp

    def get_df(self):
        return self.fit(self.X_train,self.y_train)

    def save_traindata(self,csv_dir,X_test,reply_test):
        df_train=self.X_train
        df_train['label']=self.y_train
        df_train['reply']=self.reply_train
        df_test=X_test
        df_test['label']=u'没有标签'
        df_test['reply']=reply_test
        df=pd.concat([df_train,df_test])                    #concat:对dataframe进行合并操作
        df.to_csv(csv_dir,index=False,encoding='utf8')

    def _get_labels(self,yl):
        return [self._get_label(i) for i in yl]

    def _simp_labels(self,n):
        self.y_train=[lab if len(lab.split('/'))<n else self._get_label(lab) for lab in self.y_train]

    def _y2py(self,yte):
        ytr=np.array(self._get_labels(self.y_train))
        yte=np.array(self._get_labels(yte))
        for i in range(yte.shape[0]):
            if i==0:
                py=ytr==yte[i]
            else:
                py=np.hstack((py,ytr==yte[i]))     #hstack:水平方向合并；vstack:垂直方向合并
        return py






