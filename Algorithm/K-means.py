# -*- coding: utf-8 -*-

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE       #高维数据可视化工具

def kmeans_plot():
    iris=load_iris()
    data=pd.DataFrame(iris.data)
    data_zs=(data-data.mean())/data.std()    #数据标准化
    k=3     #设置聚类数目
    iteration=500   #设置最大迭代次数
    model=KMeans(n_clusters=k,n_jobs=4,max_iter=iteration)   #创建kmeans对象
    Model=model.fit(data_zs)      #使用数据训练模型
    # pd.Series(Model.labels_).value_counts()   #每个类别样本个数
    # pd.DataFrame(Model.cluster_centers_)     #每个类别的聚类中心

    tsne=TSNE(learning_rate=100)
    Tsne=tsne.fit_transform(data_zs)          #对数据进行降维
    print Tsne
    data=pd.DataFrame(Tsne,index=data_zs.index)

    ######不同类别用不同颜色和样式绘图
    d=data[model.labels_==0]
    plt.plot(d[0],d[1],'r.')
    d=data[model.labels_==1]
    plt.plot(d[0],d[1],'go')
    d=data[model.labels_==2]
    plt.plot(d[0],d[1],'b*')
    plt.show()

if __name__=='__main__':
    kmeans_plot()


#########用PCA降维，对聚类结果进行可视化



