#!/usr/bin/env python
# coding=utf-8

from constVal import *
import re
class RegionInfo:
    racialSet = []
    racialPatternList = []
    provincePatternList = []
    cityPatternList = []
    districtPatternList = []
    streetPatternList = []
    lenToLevel = {}
    def __init__(self,regionCode,name):
        self.regionCode = regionCode
        self.level = RegionInfo.getLevelByCode(regionCode)
        self.parentRegionCode = RegionInfo.getParentCode(regionCode)
        self.fullName = name
        self.simpleName = RegionInfo.fullNameToSimpleName(self.fullName,self.level)
        self.childeRegionInfoList = []

    @staticmethod
    def initLevelLen():
        for key in levelToLen.keys():
            RegionInfo.lenToLevel[levelToLen.get(key)] = key

    @staticmethod
    def initCache():
        arr = []
        arr = allRacialStr.split(",")
        for str in arr:
            RegionInfo.racialSet.append(str)
            RegionInfo.racialPatternList.append(str)
        arr = provinceStr.split(",")
        for str in arr:
            RegionInfo.provincePatternList.append(str)
        arr = cityStr.split(",")
        for str in arr:
            RegionInfo.cityPatternList.append(str)
        arr = districtStr.split(",")
        for str in arr:
            RegionInfo.districtPatternList.append(str)
        arr = streetStr.split(",")
        for str in arr:
            RegionInfo.streetPatternList.append(str)

    @staticmethod
    def getParentCode(regionCode):
        level = RegionInfo.getLevelByCode(regionCode);
        parentLevel = level - 1;
        len = levelToLen.get(parentLevel);
        if len == None:
            return "0";
        parentCode = regionCode[0:len];
        return parentCode;

    @staticmethod
    def cityFullNameToSimpleName(fullName):
        simpleName = None
        fullName = RegionInfo.removeOnePattern(fullName, RegionInfo.cityPatternList)
        simpleName = RegionInfo.removePattern(fullName, RegionInfo.racialSet)
        return simpleName

    @staticmethod
    def districtFullNameToSimpleName(fullName):
        simpleName = None
        fullName = RegionInfo.removeOnePattern(fullName, RegionInfo.districtPatternList);
        simpleName = RegionInfo.removePattern(fullName, RegionInfo.racialPatternList);
        return simpleName
    @staticmethod
    def streetFullNameToSimpleName(fullName):
        simpleName = None
        fullName = RegionInfo.removeOnePattern(fullName, RegionInfo.streetPatternList);
        simpleName = RegionInfo.removePattern(fullName, RegionInfo.racialPatternList);
        return simpleName

    @staticmethod
    def fullNameToSimpleName(fullName,level):
        simpleName = None
        if level == 1:
            simpleName = RegionInfo.provinceFullNameToSimpleName(fullName)
        elif level == 2:
            simpleName = RegionInfo.cityFullNameToSimpleName(fullName)
        elif level == 3:
            simpleName = RegionInfo.districtFullNameToSimpleName(fullName)
        elif level == 4:
            simpleName = RegionInfo.streetFullNameToSimpleName(fullName)
        else:
            simpleName = RegionInfo.provinceFullNameToSimpleName(fullName)
            simpleName = RegionInfo.cityFullNameToSimpleName(fullName)
            simpleName = RegionInfo.districtFullNameToSimpleName(fullName)
        return simpleName

    @staticmethod
    def provinceFullNameToSimpleName(fullName):
        simpleName = None
        if fullName == '内蒙古自治区':
            simpleName = '内蒙古'
        elif fullName == "新疆维吾尔自治区":
            simpleName = '新疆'
        elif fullName == "广西壮族自治区":
            simpleName = "广西"
        elif fullName == "西藏自治区":
            simpleName = "西藏"
        else:
            simpleName = RegionInfo.removeOnePattern(fullName, RegionInfo.provincePatternList)
        return simpleName

    @staticmethod
    def removePattern(str2, patternList):

        result = str2
        for pattern in patternList:
            result = re.sub(pattern, '', result)

        if len(result) <= 1:
            result = str2

        return result

    @staticmethod
    def removeOnePattern(str2, patternList):

        result = str2
        for pattern in patternList:
            result = re.sub(pattern, '', result)
            if len(result) != len(str2):
                break

        if len(result) <= 1:
            result = str2

        return result

    @staticmethod
    def getLevelByCode(regionCode):
        len = RegionInfo.getSize(regionCode)
        if len <= 2:
            return 1
        elif len > 2 and len <= 4:
            return 2
        elif len > 4 and len <= 6:
            return 3
        elif len > 6 and len <= 9:
            return 4
        elif len > 9 and len <= 12:
            return 5
        return 0


    @staticmethod
    def getGrandpaCode(regionCode):
        level = RegionInfo.getLevelByCode(regionCode);
        parentLevel = level - 2;
        len = levelToLen.get(parentLevel);
        if len == None:
            return "0"
        parentCode = regionCode[0:len];
        return parentCode;

    def regionInfo_cmp(_,regionInfo1, regionInfo2):
        if regionInfo1.level < regionInfo2.level:
            return -1
        elif regionInfo1.level == regionInfo2.level:
            return 0
        else:
            return 1

    @staticmethod
    def getSize(str):
        count = 0
        for c in str:
            count = count + 1
        return count
    @staticmethod
    def codeFullToShort(fullCode):
        last = RegionInfo.getSize(fullCode)
        i = last - 1
        while i > -1:
            if fullCode[i] != '0':
                last = i
                break
            i = i - 1

        len = last + 1
        level = 0
        if len <= 2:
            level = 1
        elif len > 2 and len <= 4:
            level = 2
        elif len > 4 and len <= 6:
            level = 3
        elif len > 6 and len <= 9:
            level = 4
        elif len > 9 and len <= 12:
            level = 5
        shortLen = levelToLen.get(level)
        return fullCode[0:shortLen]

