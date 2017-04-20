# -*- coding: utf-8 -*-

from simhash import  Simhash
from pandas import DataFrame
import itertools
import jieba
from gensim  import corpora ,models
from Name_dict import *
from sklearn.cluster import KMeans
from scipy.spatial import distance
# A=Simhash([("I" ,1),("love",10) ,("you",3) ])
# print A.build_by_features([("I" ,1),("love",10) ,("you",3)])


def loadData():
    with open(r"sampledata.txt") as  f:
        fileText =f.read().decode("utf-8").split('|||')
    fileTextdict=[line.split("\t") for line in fileText  if len(line.split('\t'))==2]
    docdf=DataFrame(np.array(fileTextdict)[:,0],index=np.array(fileTextdict)[:,1],columns=['QA'])
    return docdf

def getStopWords():
    with  open("Ch_stopList.txt") as f:
        stop_list=f.read().decode('utf-8').split('\n')
    return  stop_list

def getRemoveStopWordOfDict(dictionary):            #token2id将每个token给定一个一一对应的id
    stop_id = [dictionary.token2id[stopword] for stopword in getStopWords() if stopword in dictionary.token2id]
    dictionary.filter_tokens(stop_id)  ##去除约200个停用词
    dictionary.filter_extremes(no_below=3, no_above=0.6)    #确定给定范围的词频数
    dictionary.compactify()           #使字典更紧致化
    return  dictionary

def getToken2TfIdf(docdf):
    documents = docdf.values.flatten()     #flatten对array进行拉直操作
    texts = [jieba.lcut(line) for line in documents]   #jieba.lcut()直接返回list
    dictionary = corpora.Dictionary(texts)    #构造一个字典对象
    dictionary=getRemoveStopWordOfDict(dictionary)
    corpus = [dictionary.doc2bow(text) for text in texts]      #将字典转化为词袋，二元组形式的一个列表
    corpus_tfidf = models.TfidfModel(corpus)
    token2id = dictionary.token2id
    id2token = dict(zip(token2id.values(), token2id.keys()))
    Token2tfidf = [[(id2token[x], y) for x, y in corpus_tfidf[line]] for line in corpus]
    return  Token2tfidf        #返回的是每个词token对应的tfidf值，形式为[[],[],...,[]]


def getSimilarityMatrix(list_like):
    Sims = map(Simhash, list_like)    #list_like为每个句子中的词的tfidf值，[[],[],[]]
    Sims_length=len(Sims)
    Similarity_Matrix=np.array([x.distance(y) for x,y in itertools.product(Sims,Sims)]).reshape((Sims_length,Sims_length))
       #itertools为一个循环器包，product相当于计算笛卡尔积
    return  1.0-Similarity_Matrix/64.0

def getTopN(Similarity_Matrix,topN=10):
    argTopN=np.argsort(-Similarity_Matrix)[:,1:topN]    #np.argsort返回排序后的索引，默认按行排
    return argTopN

## textData  必须是np.array
def getTopNInstance(textData,argTopN):
    return textData[argTopN]


if __name__ == "__main__":
    docDf=loadData().drop_duplicates()      #删除重复项
    Token2Tf=getToken2TfIdf(docDf)
    CoOccueIter = []
    p=0.1
    while  p<0.9:
        SimiMatrix=getSimilarityMatrix(Token2Tf)

        # SimiMatrix=distance.squareform(distance.pdist(SimiMatrix))
        # print SimiMatrix

        km = KMeans(n_clusters=3)
        kmClusters = km.fit(SimiMatrix)
        kmlabels = kmClusters.labels_


        argArray=getTopN(SimiMatrix,topN=10)
        # textList=docDf.values.flatten()
        textList=getS2P(docDf.index.values)   #docDf.index.values得到每个问答对应的二级标题，得到二级标题对应的一级标题的数字编号

        cluters=DataFrame(Token2Tf, index=kmlabels)
        token2TfIter=[];CoOccue=[]
        for indexIterm in cluters.index.unique():
            SomeCluster = cluters.loc[indexIterm, :].values  #loc作用于DataFrame上，指定index和column来操作
            MostCoOccue, LessCoOccue = findCoOccue(SomeCluster.ravel())  #ravel与flatten相似，但flatten相当于拷贝，而ravel不是
            SomeClusterToken2TfIdf = np.array(Token2Tf)[np.where(cluters.index.values == indexIterm)]
                  #np.where相当于三元表达式，if...else...;np.where(cond1==cond2)返回的是对应的索引值
            addMostDelLess = map(lambda x: list(set(x + MostCoOccue).difference(set(LessCoOccue))), SomeClusterToken2TfIdf)
                  #difference是对集合取差集
            token2TfIter.extend(addMostDelLess)
            CoOccue.extend(MostCoOccue+LessCoOccue)
        Token2Tf=token2TfIter

        unionTT = list(set(CoOccue).intersection(set(CoOccueIter)))
                #intersection是对集合取交集
        p = len(unionTT) / float(len(set(CoOccue+CoOccueIter)))
        print float(len(set(CoOccue+CoOccueIter)))
        print unionTT

        # threshold = 0.0
        # print CoOccue
        # for x,y in zip(CoOccue,CoOccueIter):
        #     unionTT = list(set(x).intersection(set(y)))
        #     threshold+=len(unionTT) / float(len(set(x + y)))
        p=p/3.0
        print p
        CoOccueIter=CoOccue
        print CoOccueIter






    # print argArray
    # print textList[argArray]
    # ss=DataFrame(textList[argArray],index=textList)  #.to_excel("sec1.xlsx",sheet_name="Top5")
    # ss["label"]=map(getMostCommon,ss.values)
    # ss.to_excel("sec1.xlsx",sheet_name="Top5")



