# -*- coding: utf-8 -*-

# f=open('C:\\Users\\Administrator\\Desktop\\custorm_data.csv')
# data_dic={}
# for line in f.readlines():
#     line=line.replace('\n',' ').split(',')
#     line=map(lambda x : float(x) ,line)
#     for i in range(1,len(line)):
#         if line[0] in data_dic.keys():
#             data_dic[int(line[0])].append(line[i])
#         else:
#             data_dic[int(line[0])]=[]
#             data_dic[int(line[0])].append(line[i])
# print data_dic
# f.close()

with open('C:\\Users\\Administrator\\Desktop\\22.txt') as f:
    a=f.read()
print a
f.close()

f=open('C:\\Users\\Administrator\\Desktop\\22.txt')
b=f.readline()
print b
c=f.readline()
print c
f.close()

f=open('C:\\Users\\Administrator\\Desktop\\22.txt')
d=f.readlines()
print d
f.close()

f=open('C:\\Users\\Administrator\\Desktop\\33.txt','w')
msg=['write date','to 3.txt','finish']
for m in msg:
    f.write(m)
f.close()

f=open('C:\\Users\\Administrator\\Desktop\\33.txt','w')
msg=['write date\n','to 3.txt\n','finish\n']
for m in msg:
    f.write(m)
f.close()

f=open('C:\\Users\\Administrator\\Desktop\\33.txt','w')
msg=['write date\n','to 3.txt\n','finish\n']
f.writelines(msg)
f.close()




