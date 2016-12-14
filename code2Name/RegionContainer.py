#!/usr/bin/env python
# coding=utf-8
from constVal import *
from RegionInfo import *
import  codecs
class RegionContainer:
    def __init__(self,path):
        self.regionCodeToRegionInfo = {}
        self.allNameToRegionInfoList = {}
        self.path = path

    def load(self):
        dic = open(self.path,'rb')
        for line in dic:
            line = re.sub('\n','#',line)
            line = re.sub('\t', '#', line)
            line = re.sub(',', '#', line)
            workList = line.split('#')
            shortRegionCode = ''
            fullName = ''
            if len(workList) == 5:
                if workList[2] == '地区名称':
                    continue
                fullRegionCode = workList[0]
                shortRegionCode = RegionInfo.codeFullToShort(fullRegionCode)
                fullName = workList[2]
            else:
                fullRegionCode = workList[0]
                shortRegionCode = RegionInfo.codeFullToShort(fullRegionCode)
                fullName = workList[1]

            regionInfo = RegionInfo(shortRegionCode, fullName)
            self.handleRegionInfo(regionInfo)

    def handleRegionInfo(self,regionInfo):
        if regionInfo.fullName == "市辖区" or regionInfo.fullName == "县" or regionInfo.fullName == "市辖街道" or regionInfo.fullName == "省直辖行政单位":
            grandPaName = self.getParent(regionInfo).fullName
            newFullName = ''
            if regionInfo.fullName == "市辖区" or regionInfo.fullName == "市辖街道" or regionInfo.fullName == "省直辖行政单位":
                newFullName = grandPaName + regionInfo.fullName
            elif regionInfo.fullName == "县":
                newFullName = grandPaName + '市辖县'
            regionInfo.fullName = newFullName
            regionInfo.simpleName = newFullName
        # regioncode
        self.regionCodeToRegionInfo[regionInfo.regionCode] = regionInfo

        # allName.fullName
        regionInfoList = self.allNameToRegionInfoList.get(regionInfo.fullName)
        if regionInfoList == None:
            regionInfoList=[]
            self.allNameToRegionInfoList[regionInfo.fullName] = regionInfoList

        regionInfoList.append(regionInfo)

        # allName.simple
        if regionInfo.simpleName != regionInfo.fullName:
            regionInfoList = self.allNameToRegionInfoList.get(regionInfo.simpleName)
            if regionInfoList == None:
                regionInfoList = []
                self.allNameToRegionInfoList[regionInfo.simpleName] = regionInfoList
            regionInfoList.append(regionInfo)

            # add to parent
            if regionInfo.parentRegionCode != "0":
                parentRegionInfo = self.getParent(regionInfo)
                # 没有父区域，比如中山市，东莞市 level =2 下辖直接level4 没有level3
                if parentRegionInfo == None:
                    print 'No parent change parent to grandpa.{}', regionInfo
                    parentCode = RegionInfo.grandPaCode = RegionInfo.getGrandpaCode(regionInfo.regionCode)
                    regionInfo.parentRegionCode = parentCode
                    parentRegionInfo = self.getParent(regionInfo)
                parentRegionInfo.childeRegionInfoList.append(regionInfo)
    def getChildeRegionInfoList(self):
        return self.childeRegionInfoList

    def has(self,name):
       return self.allNameToRegionInfoList.has_key(name)

    def getList(self,name):
        self.allNameToRegionInfoList.get(name)

    def getHighest(self,name):
        if name == None or len(name) == 0:
            return None
        regionList = self.allNameToRegionInfoList.get(name)
        if regionList != None:
            sorted(regionList, self.regionInfo_cmp)
            return regionList[0]
        return None

    def getSpec(self,name, level):
        if name == None or len(name) == 0:
            return None
        regionInfoList = self.allNameToRegionInfoList.get(name)
        if regionInfoList != None:
            sorted(regionInfoList, self.regionInfo_cmp)
            for regionInfo in regionInfoList:
                if regionInfo.level == level:
                    return regionInfo
        return None

    def getWithRegionCode(self,regionCode):
        return self.regionCodeToRegionInfo.get(regionCode)

    def getProCityCountyWithRegionCode(self,regionCode):
        pro = None
        city = None
        county = None
        fullCode = regionCode
        shortProvinceCode = fullCode[0:2]
        shortCityCode = fullCode[0:4]
        shortCountyCode = fullCode

        regionInfo = self.getWithRegionCode(shortProvinceCode)
        if regionInfo != None:
           pro =  regionInfo.fullName
        regionInfo = self.getWithRegionCode(shortCityCode)
        if regionInfo != None:
            city =  regionInfo.fullName
        regionInfo = self.getWithRegionCode(shortCountyCode)
        if regionInfo != None:
            county= regionInfo.fullName
        return pro,city,county

    def getWithParent(self,name, parentName):
        if name == None or len(name) == 0:
            return None
        if parentName == None or len(parentName) == 0:
            return None
        regionInfoList = self.getList(name)
        if regionInfoList == None:
            return None
        for regionInfo in regionInfoList:
            parentRegionInfo = self.getParent(regionInfo)
            if parentRegionInfo.fullName == parentName or parentRegionInfo.simpleName == parentName:
                return regionInfo
            else:
                grandpaRegionInfo = self.getParent(parentRegionInfo)
                if grandpaRegionInfo.fullName == parentName or grandpaRegionInfo.simpleName == parentName:
                    return regionInfo
        return None

    def getWithParent(self,name, parentRegionInfo):
        if parentRegionInfo == None:
            return None
        regionInfoList = self.getList(name)
        if regionInfoList == None:
            return None
        for regionInfo in regionInfoList:
            curParentRegionInfo = self.getParent(regionInfo)
            if curParentRegionInfo == parentRegionInfo:
                return regionInfo
            else:
                curGrandpaRegionInfo = self.getParent(curParentRegionInfo)
                if curGrandpaRegionInfo == parentRegionInfo:
                    return regionInfo
        return None

    def getParentWithLevel(self,regionInfo, level):
        if regionInfo == None:
            return None
        parentInfo = regionInfo
        while True:
            if parentInfo.level < level:
                return None
            elif parentInfo.level == level:
                return parentInfo
            else:
                parentInfo = self.getParent(parentInfo)

    def getParent(self,regionInfo):
        if regionInfo == None:
            return None;
        return self.getWithRegionCode(regionInfo.parentRegionCode)

    def getSpec(self,province, l2, l3):
        provinceInfo = None
        cityInfo = None
        countyInfo = None
        provinceInfo = self.getSpec(province, 1)
        dianpingL2Info = None
        dianpingL3Info = None
        if len(l2) != 0 and len(l3) != 0:
            dianpingL3Info = self.getWithParent(l3, l2)
            dianpingL2Info = self.getParent(dianpingL3Info)
            if provinceInfo == None:
                provinceinfo = self.getParentWithLevel(dianpingL2Info, 1)
            else:
                if province != self.getParentWithLevel(dianpingL2Info, 1):
                    dianpingL2Info = None
                    dianpingL3Info = None
        # 获取dianpingL2Info
        if dianpingL2Info == None:
            if provinceinfo != None:
                dianpingL2Info = self.getWithParent(l2, provinceInfo)
                if dianpingL2Info == None:
                    l2 = RegionInfo.fullNameToSimpleName(l2)
                    dianpingL2Info = self.getWithParent(l2, provinceinfo)
            else:
                dianpingL2Info = self.getHighest(l2)
                if dianpingL2Info == None:
                    l2 = RegionInfo.fullNameToSimpleName(l2)
                    dianpingL2Info = self.getHighest(l2)
                provinceinfo = self.getParentWithLevel(dianpingL2Info, 1)
                if provinceinfo != None:
                    print provinceinfo
        if dianpingL2Info != None:
            if dianpingL2Info.level == 2:
                cityInfo = dianpingL2Info
                if dianpingL3Info == None:
                    dianpingL3Info = self.getWithParent(l3, cityInfo)
                countyInfo = self.getParentWithLevel(dianpingL3Info, 3)
            elif dianpingL2Info.level == 3:
                cityInfo = self.getParent(dianpingL2Info)
                countyInfo = dianpingL2Info
        else:
            print "DianpingL2Info is null. province", province, "l2", l2, "l3", l3
        regionInfos = [provinceinfo, cityInfo, countyInfo]
        return regionInfos

    def regionCodeLenTo6(self,srcRegionCode):
        if len(srcRegionCode) == 0:
            return srcRegionCode
        desRegionCode = srcRegionCode
        if len(srcRegionCode) > 6:
            desRegionCode = srcRegionCode[0:6]
        if len(srcRegionCode) < 6:
            desRegionCode = srcRegionCode
            len = 6
            cur = len(srcRegionCode)
            while cur < len:
                desRegionCode = desRegionCode + "0"
                cur = cur + 1
        return desRegionCode
