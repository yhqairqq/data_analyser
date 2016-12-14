#!/usr/bin/env python
# coding=utf-8

import numpy as np
import codecs
from utils import *


def loadDic(file):
    content = codecs.open(file, 'r', 'utf-8')
    i = 0;
    dic = {}
    for line in content:
        items = line.split(u' ')
        dic[items[0]] = i
        i = i + 1
    return dic


def str2Vec(dic, str):
    vec = np.zeros((1, len(dic)))

    for word in str:
        index = dic.get(word)
        if index == None:
            continue
        vec[0][index] = vec[0][index] +1

    return vec


if __name__ == '__main__':
    file = '/Users/YHQ/python_pro/untitled/brandcluster/word.dic'

    dic = loadDic(file)


    #    val strings = Array("1916汉庭桌球俱乐部", "2030汉庭网吧", "三河市汉庭酒店有限公司", "上海汉庭快捷酒店", "东山汉庭假日酒店")
list = [u"1916汉庭桌球俱乐部",u"2030汉庭网吧", u"三河市汉庭酒店有限公司", u"上海汉庭快捷酒店", u"东山汉庭假日酒店",u"美加齿科科科科科科科科"]
src = u'三河市汉庭酒店有限公司'

def similarity(src,dst):
    count = 0
    for word1 in src:
        for word2 in dst:
            if word1 == word2:
                count = count+1
    return count/float(len(src))



for name in list:
   print similarity(src,name)
