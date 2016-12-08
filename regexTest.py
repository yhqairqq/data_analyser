#!/usr/bin/python
# -*- coding: UTF-8 -*-
import re
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')
# reload(sys)
# sys.setdefaultencoding('utf8')
# line = "  ＊％／@*%/@";
#
# line = u'圣世苑温泉大酒店-网球馆';
# #【（﹙\(].+[）\)﹚】
#
# line=re.sub(u'【[^】]*】', "", line)
# line=re.sub(u'（[^）]*）', "", line)
# line=re.sub(u'﹙[^﹚]*﹚', "", line)
# line=re.sub(u'\([^\)]*\)', "", line)
# index=line.index(u"-")
# if(index>=0):
#  line=line[:index]
# # line=line[:line.index(u"_")]
# print line


def check_contain_chinese(check_str):
    for ch in check_str.decode('utf-8'):
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


print check_contain_chinese('中国')
print check_contain_chinese('xxx')
print check_contain_chinese('xx中国')
#|(（[^）]*）)|


# line = re.sub(r'[*]*[＊]*[％]*[／]*[@]*[%]*[/]*[ ]*',"",line)
# if len(line) == 1 and ((line[0]>='a' and line[0]<='z') or (line[0]>='A' and line[0]<='Z')):
#     print line
#unicode chinese
# s=u"你好"
# # print(re.match(r'[0-9a-zA-Z]*', s).span())  # 在起始位置匹配
# print len(s)


# brand='你好'
# l=len(brand)
#
# if  l > 60 or l<1 or (l==1 and ((brand[0]>='a' and brand[0]<='z') or (brand[0]>='A' and brand[0]<='Z'))):
#               # fo.writelines(brand)
#     print brand



#print line