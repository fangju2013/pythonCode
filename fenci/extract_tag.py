# -*- coding: utf-8 -*-
####关键词提取：基于TF-IDF算法的关键词提取
import sys
import jieba
import jieba.analyse
from optparse import OptionParser
 #jieba.analyse.extract_tags(sentence,topK=20,withWeight=False,allowPOS=())
  #sentennce:待提取的文本
  #topK返回几个TF/IDF权重最大的关键词，默认值为20
  #withWeight为是否一并返回关键词权重值，默认值为False
  #allowPOS仅包括指定词性的词，默认值为空
#jieba.analyse.TFIDF(idf_path=None):新建TFIDF实例，idf_path为IDF频率文件
# USAGE = "usage:    python extract_tags.py [extract.txt] -k [top k]"
# parser=OptionParser(USAGE)
# parser.add_option('-k',dest='topK')
# opt,args=parser.parse_args()
#
# if len(args) < 1:
#     print USAGE
#     sys.exit(1)
#
# file_name=args[0]
#
# if opt.topK is None:
#     topK=10
# else:
#     topK=int(opt.topK)

content=open('C:\\Users\\Administrator\\Desktop\\extract.txt','rb').read()
tags=jieba.analyse.extract_tags(content,topK=30)
print ','.join(tags)

print len(tags)
