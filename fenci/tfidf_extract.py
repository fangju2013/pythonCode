# -*- coding: utf-8 -*-

import MySQLdb
import jieba
import jieba.analyse
import jieba.posseg as pseg
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host='192.168.2.83', user='zhaolijun', passwd='z8RUQrqeCWdHSn9fgAta',
                       db='crawl_analysis', port=3359, use_unicode=True, charset='utf8')
def select(sql):
    try:
        cur=conn.cursor()
        cur.execute(sql)
        return cur.fetchall()
        cur.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0],e.args[1])
        return 0

sql='select name_prd from crawl_jd_order_detail'
commodity_name=select(sql)
