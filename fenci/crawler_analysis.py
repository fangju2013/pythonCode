# -*- coding: utf-8 -*-

from __future__ import division
import MySQLdb
import jieba
import jieba.posseg as pseg
import json
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
conn = MySQLdb.connect(host='192.168.2.83', user='zhaolijun', passwd='z8RUQrqeCWdHSn9fgAta',
                       db='crawl_analysis', port=3359,use_unicode=True,charset='utf8')
def select(sql):
    try:
        cur=conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
        cur.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0],e.args[1])
        return 0

# fj_dic = dict()
# for line in data:
#     fj_dic.setdefault(line[0],[]).append(line[1])
# print fj_dic
#根据每个客户ID对应的商品来构造字典：
def set_dict(data):
    fj_dic = dict()
    for line in data:
        if line[0] in fj_dic.keys():
            fj_dic[line[0]].append(line[1])
        else:
            fj_dic[line[0]]=[]
            fj_dic[line[0]].append(line[1])
    return fj_dic

#根据每个客户ID来进行关键词提取：
def get_keyword(dic):
    key_word=dict()
    for key in dic.keys():
        values=dic[key]
        for i in range(len(values)):
            words=pseg.cut(values[i])
            for word,tag in words:
                if tag in ['n'] and len(word) in [2,3,4]:
                    if key in key_word.keys() :
                        key_word[key].append(word)
                    else:
                        key_word[key]=[]
                        key_word[key].append(word)
    return key_word

#将对每个客户分出来的词进行一个词频统计：
def word_statistic(dic):
    key_word_stat=dict()
    for key in dic.keys():
        values=dic[key]
        tmp=dict()
        for value in values:
            tmp[value]=values.count(value)
        key_word_stat[key]=tmp
    return key_word_stat

#对所有的词进行一个词频统计
 #先将所有的词拼接成一个list
def get_list(dic):
    word_list=[]
    for key in dic.keys():
        value=dic[key]
        word_list.extend(value)
    return word_list
 #再进行词频的统计
def word_freq(word_list):
    freq_word={}
    for word in word_list:
        freq_word[word]=word_list.count(word)
    return freq_word

#根据每个客户统计其关键词词频的频率
def get_word_ratio(dic1,dic2):
    word_ratio={}
    for key1 in dic1:
        value=dic1[key1]
        tmp={}
        for key2 in value.keys():
            if key2 in dic2.keys():
                tmp[key2]=value[key2]/dic2[key2]
        tmp=sorted(tmp.iteritems(), key=lambda d: d[1], reverse=True)
        word_ratio[key1]=tmp
    return word_ratio
########################################################################################
sql='select custorm_id,name_prd from crawl_jd_order_detail order by custorm_id'
data=select(sql)
set_dic=set_dict(data)
key_word=get_keyword(set_dic)
key_word_stats=word_statistic(key_word)
list1=get_list(key_word)
freq_word=word_freq(list1)
result=get_word_ratio(key_word_stats,freq_word)

#将所得数据写入到excel进行直观观察
f=open('C:\\Users\\Administrator\\Desktop\\key_word.json','w')
f.write(json.dumps(result,ensure_ascii=False))
f.close()

#将所得数据写入到csv文件中
f=open('C:\\Users\\Administrator\\Desktop\\key_word.csv','w')
for i in result:
    temp=i
    for j in result[i]:
        f.write(str(temp)+','+str(j[0])+','+str(j[1])+'\n')
f.close()

#根据每个客户ID的商品运用TF-IDF来进行关键词提取：
# def extract_tag(dic):
#     key_word=dict()
#     for key in dic.keys():
#         values=dic[key]
#         for i in range(len(values)):
#             if key in key_word.keys():
#                 key_word[key].extend(jieba.analyse.extract_tags(values[i]))
#             else:
#                 key_word[key]=[]
#                 key_word[key].extend(jieba.analyse.extract_tags(values[i]))
#     return key_word
#
# #将提取到的所有关键词拼接成一个list
# def stats_freq(key_word):
#     term_sum=[]
#     for key in key_word.keys():
#         values=key_word[key]
#         term_sum.extend(values)
#     return term_sum
#
# #统计词频
# def count_freq(list):
#     freq_stats={}
#     for item in list:
#         freq_stats[item]=list.count(item)
#     return freq_stats
#
# ##########################################################################################
# sql='select custorm_id,name_prd from crawl_jd_order_detail order by custorm_id'
# data=select(sql)
# set_dic=set_dict(data)
# extr_tag=extract_tag(set_dict(data))
# stats_fr=stats_freq(extract_tag(set_dict(data)))
# count_fr=count_freq(stats_freq(extract_tag(set_dict(data))))
# sort_fr=sorted(count_fr.iteritems(),key=lambda d:d[1],reverse=True)
# # for item in sort_fr:
# #     print '%s:%s' % (item[0],item[1])
#############################################################################################
# # f=open("C:\\Users\\Administrator\\Desktop\\key_word.json",'w')
# # f.write(json.dumps(sort_fr,ensure_ascii=False).encode("utf-8"))
# # f.close()
#
# f=open("C:\\Users\\Administrator\\Desktop\\key_word.csv",'w')
# for item in sort_fr:
#     f.write(item[0].encode('utf-8')+','+str(item[1])+'\n')
# f.close()
#关闭查询函数连接
conn.close()


#根据每个客户ID来进行关键词提取：
# def get_keyword(dic):
#     key_word=dict()
#     for key in dic.keys():
#         values=dic[key]
#         for i in range(len(values)):
#             words=jieba.cut(values[i])
#             for word in words:
#                 if key in key_word.keys() and len(word) in [2,3,4]:
#                     key_word[key].append(word)
#                 if key not in key_word.keys() and len(word) in [2,3,4]:
#                     key_word[key]=[]
#                     key_word[key].append(word)
#     return key_word

#将数据写入到csv中：
# f=open('C:\\Users\\Administrator\\Desktop\\key_word.csv','w')
# for i in result:
#     temp=i
#     for j in result[i]:
#         f.write(str(temp)+','+str(j)+','+str(result[i][j])+'\n')
# f.close()
