# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib2
from multiprocessing.dummy import Pool

def opener(url):
    User_Agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0'
    header = {}
    header['User-Agent'] = User_Agent
    req=urllib2.Request(url,headers=header)
    response=BeautifulSoup(urllib2.urlopen(req,None))
    return  response

def getMainUrl():
    list=[74,78,77,82,83,80,81,84,85,95,1101]
    mainUrlPrefix='http://iask.sina.com.cn/c/'
    mainUrlSuffix='.html'
    mainUrls=[mainUrlPrefix+str(line)+mainUrlSuffix for line in list]
    return mainUrls

def getSecondClassUrl(mainUrl):
    mainRes=opener(mainUrl)
    secondUrlTemp=mainRes.find('ul',class_='panel-body nav-pills mt10 plr20').find_all('a')
    secondUrlSuffix=[line['href'] for line in secondUrlTemp]
    urlPrefix = "http://iask.sina.com.cn"
    secondUrls=[urlPrefix+str(line) for line in secondUrlSuffix]
    return secondUrls

def getClassName(mainUrl):
    mainRes=opener(mainUrl)
    mainClass=mainRes.find('div',class_='panel-header plr20').find('h3').string.encode('utf-8').strip()
    SecondClassNameTemp=mainRes.find("ul",class_='panel-body nav-pills mt10 plr20').find_all("a")
    SecondClassNames=[line.string.encode('utf-8').strip() for line in SecondClassNameTemp]
    classNames=mainClass+'\n'+'\t'.join(SecondClassNames)+'\n'
    with open('classNames.txt','a+') as f:
        f.write(classNames)


# f=open('classNames.txt').read().split('\n')
# print f[3]


def getClassContent(secondUrl):
    urlRes=opener(secondUrl)
    className=urlRes.find('div',class_='panel-header plr20').find('h3').string.encode('utf8')
    temp=urlRes.find('div',class_='pages')
    urlPrefix = "http://iask.sina.com.cn"
    flag=1
    flagCount=int(temp['pagecount'])
    while flag<flagCount:
        try:
            urlRes = opener(secondUrl)
            urlContentTmp=urlRes.find('ul',class_='list-group').find_all('div',class_='question-title')
            urlContent=[line.text.encode('utf-8').strip()+'\t'+className.strip() for line in urlContentTmp]
            urlContent='|||'.join(urlContent)
            flag = int(urlRes.find('div',class_='pages')['ss'].split('-')[0])
            secondUrl = urlPrefix + urlRes.find('div', class_='pages').find_all('a')[-1]['href']
        except  Exception as e:
            print e
            break

        with open('content1.txt','a+') as f:
            f.write(urlContent)
        print 'Now crawel the %s class' % className
        flag+=1


# mainUrl='http://iask.sina.com.cn/c/74.html'
# print getClassName(mainUrl)
# secondUrls=getSecondClassUrl(mainUrl)
# print map(getClassContent,secondUrls)



# mainUrls=getMainUrl()
# secondTempUrls=map(getSecondClassUrl,mainUrls)
# secondUrls=[]
# for line in secondTempUrls:
#     secondUrls.extend(line)
# with open('mainUrl.txt','a+') as f:
#     for line in secondUrls:
#         f.write(str(line))
#         f.write('\n')

##########################get className
# mainUrls=getMainUrl()
# map(getClassName,mainUrls)

########################################################
def main():
    f=open('mainUrl.txt','r')
    mainUrl=[]
    for line in f.readlines():
        mainUrl.append(line.strip())
    f.close()
    print mainUrl
    pool = Pool(8)
    try:
        pool.map(getClassContent, mainUrl)
    except:
        print '未知错误'
    pool.close()
    pool.join()

if __name__=='__main__':
    main()


# f=open('content1.txt').read().split('|||')
# print f[1].split('\t')[1]




