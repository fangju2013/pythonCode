# -*- coding: utf-8 -*-

from Functions import dfsavedir
from Learn_model import dpf,X_test,test_reply,slr,useful

for i in range(1000):
    addX=X_test.iloc[[0]]
    reply=test_reply[0]
    if len(reply)>5:
        X_train=dpf.fit_x(addX)
        prob=slr.predict_proba(X_train)[:0]
        df=dpf.get_most_similar_reply(addX,reply,prob,n=5)
        df=dpf.get_df()
        X_train=df[useful]
        y_train=df['plabel'].astype(int)
        slr.fit(X_train,y_train)
    X_test=X_test[1:]
    test_reply=test_reply[1:]
    flag=raw_input('if you want quit then enter "q" else continue......................................')
    if flag=='q':
        break

dpf.save_traindata(dfsavedir,X_test,test_reply)
