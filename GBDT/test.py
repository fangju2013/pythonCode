# -*- coding: utf-8 -*-

from __future__ import division
import datetime
from sklearn.datasets import make_hastie_10_2
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
X, y = make_hastie_10_2(random_state=0)
X_train, X_test = X[:2000], X[2000:]
y_train, y_test = y[:2000], y[2000:]
x,y = X_train,y_train
#--------------------------------------------------------------------------------------
print ('test my least square gbt')
a = datetime.datetime.now()
from gbdt import Sgbt
slf = Sgbt(depth=1,minisamp=50,precise=2,rounds=500,eta=1,fittype='lg',earlystop=0.001)
slf.fit(X_train,y_train)
b = datetime.datetime.now()
print (b-a)
ypred = slf.predict(X_test)
print(roc_auc_score(y_test,ypred))
b = datetime.datetime.now()
print (b-a)
#--------------------------------------------------------------------------------------
print ('test sklearn gbt')
a = datetime.datetime.now()
clf = GradientBoostingClassifier(n_estimators=500, learning_rate=1,
     max_depth=1, random_state=0).fit(X_train, y_train)
b = datetime.datetime.now()
print (b-a)
ypred = clf.predict_proba(X_test)[:,1]
print (roc_auc_score(y_test,ypred))
b = datetime.datetime.now()
print (b-a)