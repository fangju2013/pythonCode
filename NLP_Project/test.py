# -*- coding: utf-8 -*-

# from sklearn.learning_curve import validation_curve
# from sklearn.pipeline import Pipeline
# from sklearn.linear_model import SGDClassifier
#
# import pandas as pd
# import numpy as np
# from Functions import dfsavedir
# from collections import Counter
#
# df=pd.read_csv(dfsavedir,encoding='utf8')
# train_df=df[df['label']!=u'没有标签']
# test_df=df[df['label']==u'没有标签']
# useful=list(df.columns)
# for i in ['label','reply']:
#     useful.remove(i)
# X_train=train_df[useful].astype(int)
# y_train=list(train_df['label'])
#
# train_reply=list(np.array(train_df.reply))
# test_reply=list(np.array(test_df.reply))
#
# def get_label(y):
#     y_label=[]
#     for i in y:
#         tmp=i.split('/')
#         y_label.append(tmp[0])
#     return y_label
#
# for i in  get_label(y_train):
#     print i
#
#
# # print X_train
# print X_train.iloc[[0]]


from __future__ import print_function
import numpy as np

from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_footer
from sklearn.datasets.twenty_newsgroups import strip_newsgroup_quoting
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

class ItemSelector(BaseEstimator,TransformerMixin):
    def __init__(self,key):
        self.key=key

    def fit(self,x,y=None):
        return self

    def transform(self,data_dict):
        return data_dict[self.key]

class TextStats(BaseEstimator,TransformerMixin):
    def fit(self,x,y=None):
        return self

    def transform(self,posts):
        return [{'length':len(text),
                 'num_sentences':text.count('.')}
                for text in posts]

class SubjectBodyExtractor(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, posts):
        features = np.recarray(shape=(len(posts),),
                               dtype=[('subject', object), ('body', object)])
        for i, text in enumerate(posts):
            headers, _, bod = text.partition('\n\n')
            bod = strip_newsgroup_footer(bod)
            bod = strip_newsgroup_quoting(bod)
            features['body'][i] = bod

            prefix = 'Subject:'
            sub = ''
            for line in headers.split('\n'):
                if line.startswith(prefix):
                    sub = line[len(prefix):]
                    break
            features['subject'][i] = sub

        return features

pipeline = Pipeline([
    ('subjectbody', SubjectBodyExtractor()),
    ('union', FeatureUnion(
        transformer_list=[
            ('subject', Pipeline([
                ('selector', ItemSelector(key='subject')),
                ('tfidf', TfidfVectorizer(min_df=50)),
            ])),
            ('body_bow', Pipeline([
                ('selector', ItemSelector(key='body')),
                ('tfidf', TfidfVectorizer()),
                ('best', TruncatedSVD(n_components=50)),
            ])),
            ('body_stats', Pipeline([
                ('selector', ItemSelector(key='body')),
                ('stats', TextStats()),  # returns a list of dicts
                ('vect', DictVectorizer()),  # list of dicts -> feature matrix
            ])),

        ],
        transformer_weights={
            'subject': 0.8,
            'body_bow': 0.5,
            'body_stats': 1.0,
        },
    )),
    ('svc', SVC(kernel='linear')),
])

categories = ['alt.atheism', 'talk.religion.misc']
train = fetch_20newsgroups(random_state=1,
                           subset='train',
                           categories=categories,
                           )
test = fetch_20newsgroups(random_state=1,
                          subset='test',
                          categories=categories,
                          )

pipeline.fit(train.data, train.target)
y = pipeline.predict(test.data)
print(classification_report(y, test.target))
