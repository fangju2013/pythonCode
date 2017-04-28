# -*- coding: utf-8 -*-

def huffmanTree(a):                  #a为一个dict
    a = sorted(a.iteritems(),key = lambda d:d[1],reverse = False)
    while len(a)>1:
        node = (a[1][0],a[0][0]),a[1][1]+a[0][1]
        a.pop(0)
        a.pop(0)
        a.append(node)
        a=sorted(a,key = lambda d:d[1],reverse = False)
    return a[0][0]

##e.g:
# a={'I':15,'like':8,'watch':6,'brizal':5,'football':3,'worldcup':1}
# print huffmanTree(a)

def HuffManCode(a):
    a = sorted(a.iteritems(), key=lambda d: d[1], reverse=False)
    while 2 > 1:
        node = (a[1][0], a[0][0]), a[0][1] + a[1][1]
        a.pop(0)
        a.pop(0)
        if len(a) == 0:
            break
        if node[1] > a[-1][1]:
            a.append(node)
        else:
            for i in range(len(a)):
                if a[i][1] >= node[1]:
                    a.insert(i, node)
                    break
    node = node[0]
    huffmanCode = {}

    def huffcode(node, code):
        leftnode = node[0]
        rightnode = node[1]
        if isinstance(leftnode, str) or isinstance(leftnode, unicode):
            huffmanCode[leftnode] = code + '0'
        else:
            huffcode(leftnode, code + '0')
        if isinstance(rightnode, str) or isinstance(rightnode, unicode):
            huffmanCode[rightnode] = code + '1'
        else:
            huffcode(rightnode, code + '1')
    huffcode(node, '')
    return huffmanCode

def getMaxCodeLen(wordDict):
    huffmanCode=HuffManCode(wordDict)
    huffCode=huffmanCode.values()
    codeLen=[]
    for code in huffCode:
        codeLen.append(len(code))
    maxCodeLen=max(codeLen)
    return maxCodeLen

def getCodeList(str):
    codeList=[]
    for i in str:
        codeList.append(int(i))
    return codeList


###############################################
#e.g:
# words={'I':15,'like':8,'watch':6,'Brazil':5,'football':3,'worldcup':1}
# print HuffManCode(words)

