# -*- coding: utf-8 -*-

import csv
import jieba
import jieba.posseg as pseg

def tmpfunc(x,a):
    if x in a:
        return 1
    else:
        return 0

##用csv读取数据
csvfile=file('C:\\Users\\Administrator\\Desktop\\consume_statistic.csv','rb')
rawdata=csv.reader(csvfile)
next(rawdata)   #相当于从第二行开始操作数据
#####对文本进行分词，并标注词性，然后构建一个list
def get_feature(rawdata):
    feature=list()
    for line in rawdata:
        line_split=line[0].split(';')
        for lin in line_split:
            cut=pseg.cut(lin)
            for word,tag in cut:
                if 'var'+word not in feature and len(word) in [2,3,4]:
                    feature.append('var'+word)
                if 'tag_'+tag not in feature:
                    feature.append('tag_'+tag)
    return feature
feature=get_feature(rawdata)
csvfile.close()


csvfile=file('C:\\Users\\Administrator\\Desktop\\consume_statistic.csv','rb')
rawdata1=csv.reader(csvfile)
next(rawdata1)
def get_data_list(rawdata1):
    data=list()
    for line in rawdata1:
        line_split=line[0].split(';')
        for lin in line_split:
            cut=pseg.cut(lin)
            word_list=list()
            tag_list=list()
            tsq_list=list()
            for word,tag in cut:
                word_list.append('var'+word)
                tag_list.append('tag_'+tag)
                if tag in ['n','v','r'] and tag not in tsq_list:
                    tsq_list.append(tag)
            f=map(lambda x:tmpfunc(x,word_list+tag_list),feature)
            f.append(len(word_list))
            f.append(''.join(tsq_list))
            f.append(line[1])
            f.append(line[0])
            data.append(tuple(f))
    return data
data=get_data_list(rawdata1)
csvfile.close()

csvfile=file('C:\\Users\\Administrator\\Desktop\\consume_statistic.csv','rb')
writer=csv.writer(csvfile)
for i in ['wcount','tagseq','lable','reply']:
    feature.append(i)

import sys
stdout=sys.stdout
reload(sys)
sys.setdefaultencoding('utf8')
writer.writerow(feature)
writer.writerows(data)
csvfile.close()
sys.stdout=stdout



