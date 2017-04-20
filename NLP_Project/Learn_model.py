# -*- coding: utf-8 -*-

from sklearn.learning_curve import validation_curve
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier


import pandas as pd
import numpy as np
from Functions import dfsavedir
from Objects import df2distdf

df=pd.read_csv(dfsavedir,encoding='utf8')
train_df=df[df['label']!=u'没有标签']
test_df=df[df['label']==u'没有标签']
useful=list(df.columns)
for i in ['label','reply']:
    useful.remove(i)

X_train=train_df[useful].astype(int)        #astype针对np.array的字符类型转换
y_train=list(train_df['label'])
X_test=test_df[useful].astype(int)

train_reply=list(np.array(train_df.reply))
test_reply=list(np.array(test_df.reply))

dpf=df2distdf(X_train,y_train,train_reply)
df=dpf.fit(X_train,y_train)

X_train=df[useful]
y_train=df['plabel'].astype(int)

pipe_lr=Pipeline([('clf',SGDClassifier(loss='log',random_state=0,l1_ratio=0.5))])
param_range=[0.00001,0.0001,0.001,0.01,0.1,1,10,100,1000]
for k in range(3):
    train_scores,test_scores=validation_curve(
        estimator=pipe_lr,
        X=X_train,
        y=y_train,
        param_name='clf__alpha',
        param_range=param_range,
        scoring='roc_auc',
        cv=4
        )
    test_mean=np.mean(test_scores,axis=1)
    a=np.where(test_mean==max(test_mean))
    c=param_range[a[0][0]]
    print c,max(test_mean)
    param_range=[c+i*c for i in range(10)]+[c-i*0.1*c for i in range(10)]

slr=SGDClassifier(loss='log',random_state=0,alpha=c,l1_ratio=0.5)
slr.fit(X_train,y_train)


