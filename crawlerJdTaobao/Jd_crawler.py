# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2

def opener(url):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    req=urllib2.Request(url,headers=header)
    response=BeautifulSoup(urllib2.urlopen(req,None))
    return  response

# mainUrl = 'https://www.jd.com/'
# mainRes = opener(mainUrl)
# mainClassString = mainRes.find('ul',class_ = 'JS_navCtn cate_menu').find_all('li',class_ = 'cate_menu_item')
# # mainTag = []
# # for tag in mainClassString:
# #     mainTag.append(tag['clstag'])
# mainClass = [line.text.encode('utf8') for line in mainClassString]
# for Class in mainClass:
#     print Class

###################################################################################
page = open('page.html','r').read()
soup = BeautifulSoup(page, 'html.parser')
mainClassString = soup.find('ul',class_ = 'JS_navCtn cate_menu').find_all('li',class_ = 'cate_menu_item')
mainClass = [line.text.encode('utf8') for line in mainClassString]   #get the main class

secondClass = soup.find_all('div',class_ = 'cate_detail')   #get the ssecond class
secondClassCate = []
for line in secondClass:
    secondClassCate.append(line.find_all('dt',class_ = 'cate_detail_tit'))
# print secondClassCate

secondClassCateAll = []
for line1 in secondClassCate:
    secondClassCateAllTmp = [line.text.encode('utf8') for line in line1]
    secondClassCateAll.append(secondClassCateAllTmp)

mainSec = zip(mainClass,secondClassCateAll)
print mainSec

# f = open('secondClassName1.txt','w')
# for line1 in secondClassCateAll:
#     for line2 in line1:
#         f.write(line2)
#     f.write('\n')
# f.close()


secondClassCateUrl = []
for i in [0,1,2,3,4,5,7,8,9,10,11,14]:
    secondClassCateAllTmp = [line.find('a')['href'] for line in secondClassCate[i]]
    secondClassCateUrl.append(secondClassCateAllTmp)
# print secondClassCateUrl

secondClassCateUrlAll = []
for line in secondClassCateUrl:
    tmp = []
    for url in line:
        tmp1 = url.split('//')[0]
        if tmp1 is u'':
            tmp.append('https:'+url)
        else:
            tmp.append(url)
    secondClassCateUrlAll.append(tmp)
# print secondClassCateUrlAll
#
# thirdUrl = secondClassCateUrlAll[0][1]
# thirdRes = opener(thirdUrl)
# thirdClassString = thirdRes.find('div',class_ = 'sl-v-logos').find_all('li')
# # mainTag = []
# # for tag in mainClassString:
# #     mainTag.append(tag['clstag'])
# brandClass = [line.text.encode('utf8') for line in thirdClassString]
# for brand in brandClass:
#     print brand