#!/usr/bin/env python
# coding=utf-8
import  re
import codecs
class RegionInfo:
    def __init__(self):
        self.racialSet = []
        self.racialPatternList = []
        self.racialSet = []
        self.provincePatternList = []
        self.cityPatternList = []
        self.districtPatternList = []
        self.streetPatternList = []
        self.regionCode=None;
        self.parentRegionCode=None;
        self.fullName=None;
        self.simpleName=None;
        self.level=None;
        self.childeRegionInfoList=[]
class RegionContainner:
    def __init__(self):
        self.regionCodeToRegionInfo = {}
        self.allNameToRegionInfoList = {}

class classA:
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.colors = ['red','blue','black']
    def getFirstColor(self):
        if len(self.colors) > 0:
            return self.colors[0]
class A:
    def __init__(_,age1,age2):
        _.age1 = age1
        _.age2 = age2
        _.age3 = A.add(_.age1,_.age2)
    @staticmethod
    def add(age1,age2):
        return age1+age2
    @staticmethod
    def getSize(str):
        count = 0
        for c in str:
            count = count +1
        print count
if __name__ == '__main__':
    # a = classA("yang",12)
    # print a.getFirstColor()
    # fi = open('/Users/YHQ/python_pro/untitled/code2Name/region.dic','r')
    #  a = A(1,2)
    name =   u'你好'.encode('utf-8')
    print name

