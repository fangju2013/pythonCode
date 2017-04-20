# -*- coding: utf-8 -*-

import numpy as np
import lda
import matplotlib.pyplot as plt

#to convert the topic words for all the documents
X = lda.datasets.load_reuters()
vocab = lda.datasets.load_reuters_vocab()
titles = lda.datasets.load_reuters_titles()
model = lda.LDA(n_topics = 20, n_iter = 1500, random_state = 1)
model.fit(X)
topic_word = model.topic_word_
n_topic_word = 8
for i,topic_dict in enumerate(topic_word):
    topic_words = np.array(vocab)[np.argsort(topic_dict)][:-n_topic_word:-1]
    print 'Topic {}:{}'.format(i,' '.join(topic_words))

#to convert the documents which is coming from the topic word
doc_topic = model.doc_topic_
for i in range(10):
    print '{} (top topic: {})'.format(titles[i],doc_topic[i].argmax())

#train and test the model
X = lda.datasets.load_reuters()
titles = lda.datasets.load_reuters_titles()
X_train = X[10:]
X_test = X[:10]
titles_test = titles[:10]
model = lda.LDA(n_topics = 20, n_iter = 1500, random_state = 1)
model.fit(X_train)
doc_topic_test = model.transform(X_test)
for title,topics in zip(titles_test,doc_topic_test):
    print '{} (top topic:{})'.format(title,topics.argmax())

#plot the fiture of the loglikelihood values
plt.plot(model.loglikelihoods_[5:])
plt.show()