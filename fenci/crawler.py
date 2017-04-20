# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import urllib2
import csv
import time
csvfile = file('C:/Users/Administrator/Desktop/crawl_ask_reply0824pm.csv', 'wb')
writer = csv.writer(csvfile)
words = '消费贷款'
writer.writerow(['ask', 'reply'])
remain = range(1, 2684/10)
while len(remain) > 0:
    for page in remain[:]:
        goon = False
        print "pageNum:", page
        try:
            url = "http://www.rong360.com/ask/tag/" + words + "?q=&pn=" + str(page)
            url_con = BeautifulSoup(urllib2.urlopen(url))
            ask_hrefs = [line["href"] for line in url_con.find("ul", class_="search_list").find_all("a")]
            goon = True
        except:
            time.sleep(30)

        if goon:
            for ask in ask_hrefs:
                try:
                    ask_title = \
                    BeautifulSoup(urllib2.urlopen(ask)).find_all("h2", class_="title reply_question_title clearfix")[
                        0].text.encode('utf8')
                    ask_text = BeautifulSoup(urllib2.urlopen(ask)).find_all("div", class_="reply_content")[
                        0].text.encode('utf8')
                    writer.writerow([ask_title, ask_text])
                    remain.remove(page)
                except:
                    next
csvfile.close()
