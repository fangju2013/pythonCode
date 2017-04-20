# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
from multiprocessing.dummy import Pool


# url="http://wenda.so.com/c/24?pn=1"
# req = urllib2.Request(url,headers=header)
# response=urllib2.urlopen(req,None)
# ss=BeautifulSoup(response)

def opener(url):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    req=urllib2.Request(url,headers=header)
    response=BeautifulSoup(urllib2.urlopen(req,None))
    return  response

def getMainClassUrl():
    classId=range(1,2)
    urlPrefix='http://wenda.so.com/c/'
    MainClassUrl=[urlPrefix+str(id) for id in classId]
    return MainClassUrl

def getSecondClassUrl(mainUrl):
    mainRes=opener(mainUrl)
    secondUrlTemp=mainRes.find('ul',class_='sec-cate clearfix').find_all('a')
    secondUrlSuffix=[line['href'] for line in secondUrlTemp]
    urlPrefix = "http://wenda.so.com"
    secondUrls=[urlPrefix+str(line) for line in secondUrlSuffix]
    return secondUrls

def getClassName(mainUrl):
    mainRes=opener(mainUrl)
    mainHref=mainUrl.split('com')[1]
    mainClassName=mainRes.find('a',href=mainHref).string.encode('utf-8')
    SecondClassNameTemp=mainRes.find("ul",class_='sec-cate clearfix').find_all("a")
    SecondClassNames=[line.string.encode('utf-8') for line in SecondClassNameTemp]
    classNames=mainClassName+"\n"+ "\t".join(SecondClassNames)
    return classNames

# with open('url.txt','a+') as f:
#     for classUrl in getMainClassUrl():
#         secondUrls=getSecondClassUrl(classUrl)
#         for secondUrl in secondUrls:
#             thirdUrls=getSecondClassUrl(secondUrl)
#             for thirdUrl in thirdUrls:
#                 f.write(thirdUrl+'\n')

def getClassUrl():
    mainClassUrls=getMainClassUrl()
    classUrls=map(getSecondClassUrl,mainClassUrls)
    return classUrls

print [line.split("com")[1] for line in getMainClassUrl()]
print getSecondClassUrl("http://wenda.so.com/c/1")
print getClassUrl()


# def get_ask(num):
#     page=0
#     while page==1000:
#
#         User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
#         header = {}
#         header['User-Agent'] = User_Agent
#         url="http://wenda.so.com/c/" + str(num) + "?pn=" + str(page)
#         req=urllib2.Request(url,headers=header)
#         try:
#             url_class=BeautifulSoup(urllib2.urlopen(req,None))
#             ask_href=url_class.find_all('p',class_='fl qus-title')
#         except Exception as e:
#             print e
#
#         for ask in ask_href:
#             with open("%s.txt" % num , "a+") as f:
#                 f.write(ask.text.encode('utf8'))
#                 f.write("\t\t\t")
#
#         if page<=99:
#             page += 1
#         else:
#             page = 1000
#         page= page+1 if page<
#         if page%20==0:
#             print "Now %s is crawl %d  pages" % (num, page)
#
#
# if __name__ == "__main__":
#     wordlist = range(1,574)
#     pool = Pool(6)
#     pool.map(get_ask, wordlist)
#     pool.close()
#     pool.join()









