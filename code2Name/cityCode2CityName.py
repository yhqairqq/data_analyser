# #!/usr/bin/env python
# # coding=utf-8
# import codecs
# import re
# levelToLen = {1:2,2:4,3:6,4:9,5:12}
# allRacialStr = "汉族,蒙古族,回族,藏族,维吾尔族,苗族,彝族,壮族,布依族,朝鲜族,满族,侗族,瑶族,白族,土家族,哈尼族,哈萨克族,傣族,黎族,僳僳族,佤族,畲族,高山族,拉祜族,水族,东乡族,纳西族,景颇族,柯尔克孜族,土族,达斡尔族,仫佬族,羌族,布朗族,撒拉族,毛南族,仡佬族,锡伯族,阿昌族,普米族,塔吉克族,怒族,乌孜别克族,俄罗斯族,鄂温克族,德昂族,保安族,裕固族,京族,塔塔尔族,独龙族,鄂伦春族,赫哲族,门巴族,珞巴族,基诺族"
# provinceStr = "省,市,自治区,特别行政区,地区"
# cityStr = "市,自治州,州,盟"
# districtStr = "自治县,县,区,旗,市"
# streetStr = "自治乡,乡,镇,街道办事处,街道"
#
# class RegionInfo:
#     racialSet = []
#     racialPatternList = []
#     provincePatternList = []
#     cityPatternList = []
#     districtPatternList = []
#     streetPatternList = []
#     def __init__(self):
#         self.regionCode=None;
#         self.parentRegionCode=None;
#         self.fullName=None;
#         self.simpleName=None;
#         self.level=None;
#         self.childeRegionInfoList=[]
#         self.lenToLevel={}
#     def __init__(self,regionCode,name):
#         self.regionCode = regionCode
#         self.parentRegionCode = self.getParentCode(regionCode);
#         self.fullName = name
#         self.simpleName = self.fullNameToSimpleName(self.fullName,self.level)
#         self.level = RegionInfo.getLevelByCode(regionCode);
#         self.childeRegionInfoList = []
#         self.lenToLevel = {}
#     @staticmethod
#     def initLevelLen(self):
#         for key in levelToLen.keys():
#             self.lenToLevel[levelToLen.get(key)] = key
#
#     @staticmethod
#     def initCache(allRacialStr):
#         arr = []
#         arr = allRacialStr.split(",")
#         for str in arr:
#             RegionInfo.racialSet.append(str)
#             RegionInfo.racialPatternList.append(str)
#
#         arr = provinceStr.split(",")
#         for str in arr:
#             RegionInfo.provincePatternList.append(str)
#
#         arr = cityStr.split(",")
#         for str in arr:
#             RegionInfo.cityPatternList.append(str)
#         arr = districtStr.split(",")
#         for str in arr:
#             RegionInfo.districtPatternList.append(str)
#         arr = streetStr.split(",")
#         for str in arr:
#             RegionInfo.streetPatternList.append(str)
#
#     @staticmethod
#     def getParentCode(regionCode):
#         level = RegionInfo.getLevelByCode(regionCode);
#         parentLevel = level - 1;
#         len = levelToLen.get(parentLevel);
#         if len == None:
#             return "0";
#         parentCode = regionCode[0:len];
#         return parentCode;
#
#     @staticmethod
#     def cityFullNameToSimple(fullName):
#         simpleName = None
#         fullName = RegionInfo.removeOnePattern(fullName, RegionInfo.cityPatternList)
#         simpleName = RegionInfo.removePattern(fullName, RegionInfo.racialSet)
#         return simpleName
#
#     @staticmethod
#     def districtFullNameToSimpleName(fullName):
#         simpleName = None
#         fullName = RegionInfo.removeOnePattern(fullName, RegionInfo.districtPatternList);
#         simpleName = RegionInfo.removePattern(fullName, RegionInfo.racialPatternList);
#         return simpleName
#     @staticmethod
#     def streetFullNameToSimpleName(fullName):
#         simpleName = None
#         fullName = RegionInfo.removeOnePattern(fullName, RegionInfo.streetPatternList);
#         simpleName = RegionInfo.removePattern(fullName, RegionInfo.racialPatternList);
#         return simpleName
#
#     @staticmethod
#     def fullNameToSimpleName(fullName, level):
#         simpleName = None
#         if level == 1:
#             simpleName = RegionInfo.provinceFullNameToSimpleName(fullName)
#         elif level == 2:
#             simpleName = RegionInfo.cityFullNameToSimple(fullName)
#         elif level == 3:
#             simpleName = RegionInfo.districtFullNameToSimpleName(fullName)
#         elif level == 4:
#             simpleName = RegionInfo.streetFullNameToSimpleName(fullName)
#
#         return simpleName
#
#     @staticmethod
#     def provinceFullNameToSimpleName(fullName):
#         simpleName = None
#         if fullName == '内蒙古自治区':
#             simpleName = '内蒙古'
#         elif fullName == "新疆维吾尔自治区":
#             simpleName = '新疆'
#         elif fullName == "广西壮族自治区":
#             simpleName = "广西"
#         elif fullName == "西藏自治区":
#             simpleName = "西藏"
#         else:
#             simpleName = RegionInfo.removeOnePattern(fullName, RegionInfo.provincePatternList)
#         return simpleName
#
#     @staticmethod
#     def removePattern(_,str2, patternList):
#
#         result = str2
#         for pattern in patternList:
#             result = re.sub(pattern, '', result)
#
#         if len(result) <= 1:
#             result = str2
#
#         return result
#
#     @staticmethod
#     def removeOnePattern(str2, patternList):
#
#         result = str2
#         for pattern in patternList:
#             result = re.sub(pattern, '', result)
#             if len(result) != len(str2):
#                 break
#
#         if len(result) <= 1:
#             result = str2
#
#         return result
#
#     @staticmethod
#     def getLevelByCode(regionCode):
#         len = len(regionCode)
#         if len <= 2:
#             return 1
#         elif len > 2 and len <= 4:
#             return 2
#         elif len > 4 and len <= 6:
#             return 3
#         elif len > 6 and len <= 9:
#             return 4
#         elif len > 9 and len <= 12:
#             return 5
#         return 0
#
#     @staticmethod
#     def fullNameToSimpleName(fullName):
#         fullName = RegionInfo.provinceFullNameToSimpleName(fullName)
#         fullName = RegionInfo.cityFullNameToSimple(fullName)
#         fullName = RegionInfo.districtFullNameToSimpleName(fullName)
#         return fullName
#
#     @staticmethod
#     def getGrandpaCode(regionCode):
#         level = RegionInfo.getLevelByCode(regionCode);
#         parentLevel = level - 2;
#         len = levelToLen.get(parentLevel);
#         if len == None:
#             return "0"
#         parentCode = regionCode[0:len];
#         return parentCode;
#
#     def regionInfo_cmp(_,regionInfo1, regionInfo2):
#         if regionInfo1.level < regionInfo2.level:
#             return -1
#         elif regionInfo1.level == regionInfo2.level:
#             return 0
#         else:
#             return 1
#
#     @staticmethod
#     def codeFullToShort(fullCode):
#         last = len(fullCode)
#         i = last - 1
#         while i > -1:
#             if fullCode[i] == '0':
#                 last = i
#                 break
#             i = i - 1
#
#         len = last + 1
#         level = 0
#         if len <= 2:
#             level = 1
#         elif len > 2 and len <= 4:
#             level = 2
#         elif len > 4 and len <= 6:
#             level = 3
#         elif len > 6 and len <= 9:
#             level = 4
#         elif len > 9 and len <= 12:
#             level = 5
#         shortLen = levelToLen.get(level)
#         return fullCode[0:shortLen]
#
#
# class RegionContainer:
#     def __init__(self,path):
#         self.regionCodeToRegionInfo = {}
#         self.allNameToRegionInfoList = {}
#         self.path = path
#
#     def load(self,path):
#         dic =  codecs.open(path,'w','utf-8')
#         for line in dic:
#             workList = line.split('\t|\s|,')
#             shortRegionCode = ''
#             fullName = ''
#             if len(workList) == 5:
#                 if workList[2] == '地区名称':
#                     continue
#                 fullRegionCode = workList[0]
#                 shortRegionCode = RegionInfo.codeFullToShort(fullRegionCode)
#                 fullName = workList[2]
#             else:
#                 fullRegionCode = workList[0]
#                 shortRegionCode = RegionInfo.codeFullToShort(fullRegionCode)
#                 fullName = workList[1]
#
#             regionInfo = RegionInfo(shortRegionCode, fullName)
#             self.handleRegionInfo(regionInfo)
#
#     def handleRegionInfo(self,regionInfo):
#         if regionInfo.fullName == "市辖区" or regionInfo.fullName == "县" or regionInfo.fullName == "市辖街道" or regionInfo.fullName == "省直辖行政单位":
#             grandPaName = self.getParent(regionInfo).fullName
#             newFullName = ''
#             if regionInfo.fullName == "市辖区" or regionInfo.fullName == "市辖街道" or regionInfo.fullName == "省直辖行政单位":
#                 newFullName = grandPaName + regionInfo.fullName
#             elif regionInfo.fullName == "县":
#                 newFullName = grandPaName + '市辖县'
#             regionInfo.fullName = newFullName
#             regionInfo.simpleName = newFullName
#         # regioncode
#         self.regionCodeToRegionInfo[regionInfo.regionCode] = regionInfo
#
#         # allName.fullName
#         regionInfoList = self.allNameToRegionInfoList.get(regionInfo.getFullName)
#         if regionInfoList == None:
#             self.allNameToRegionInfoList[regionInfo.getFullName] = regionInfoList
#
#         regionInfoList.append(regionInfo)
#
#         # allName.simple
#         if regionInfo.simpleName == regionInfo.fullName:
#             regionInfoList = self.allNameToRegionInfoList.get(regionInfo.simpleName)
#             if regionInfoList == None:
#                 self.allNameToRegionInfoList[regionInfo.simpleName] = regionInfoList
#             regionInfoList.append(regionInfo)
#
#             # add to parent
#             if regionInfo.parentRegionCode == "0":
#                 parentRegionInfo = self.getParent(regionInfo)
#                 # 没有父区域，比如中山市，东莞市 level =2 下辖直接level4 没有level3
#                 if parentRegionInfo == None:
#                     print 'No parent change parent to grandpa.{}', regionInfo
#                     parentCode = RegionInfo.grandPaCode = RegionInfo.getGrandpaCode(regionInfo.regionCode)
#                     regionInfo.parentRegionCode = parentCode
#                     parentRegionInfo = self.getParent(regionInfo)
#                 parentRegionInfo.getChildeRegionInfoList.append(regionInfo)
#     def getChildeRegionInfoList(self):
#         return self.childeRegionInfoList
#
#     def has(self,name):
#        return self.allNameToRegionInfoList.has_key(name)
#
#     def getList(self,name):
#         self.allNameToRegionInfoList.get(name)
#
#     def getHighest(self,name):
#         if name == None or len(name) == 0:
#             return None
#         regionList = self.allNameToRegionInfoList.get(name)
#         if regionList != None:
#             sorted(regionList, self.regionInfo_cmp)
#             return regionList[0]
#         return None
#
#     def getSpec(self,name, level):
#         if name == None or len(name) == 0:
#             return None
#         regionInfoList = self.allNameToRegionInfoList.get(name)
#         if regionInfoList != None:
#             sorted(regionInfoList, self.regionInfo_cmp)
#             for regionInfo in regionInfoList:
#                 if regionInfo.level == level:
#                     return regionInfo
#         return None
#
#     def getWithRegionCode(self,regionCode):
#         return self.regionCodeToRegionInfo.get(regionCode)
#
#     def getWithParent(self,name, parentName):
#         if name == None or len(name) == 0:
#             return None
#         if parentName == None or len(parentName) == 0:
#             return None
#         regionInfoList = self.getList(name)
#         if regionInfoList == None:
#             return None
#         for regionInfo in regionInfoList:
#             parentRegionInfo = self.getParent(regionInfo)
#             if parentRegionInfo.fullName == parentName or parentRegionInfo.simpleName == parentName:
#                 return regionInfo
#             else:
#                 grandpaRegionInfo = self.getParent(parentRegionInfo)
#                 if grandpaRegionInfo.fullName == parentName or grandpaRegionInfo.simpleName == parentName:
#                     return regionInfo
#         return None
#
#     def getWithParent(self,name, parentRegionInfo):
#         if parentRegionInfo == None:
#             return None
#         regionInfoList = self.getList(name)
#         if regionInfoList == None:
#             return None
#         for regionInfo in regionInfoList:
#             curParentRegionInfo = self.getParent(regionInfo)
#             if curParentRegionInfo == parentRegionInfo:
#                 return regionInfo
#             else:
#                 curGrandpaRegionInfo = self.getParent(curParentRegionInfo)
#                 if curGrandpaRegionInfo == parentRegionInfo:
#                     return regionInfo
#         return None
#
#     def getParentWithLevel(self,regionInfo, level):
#         if regionInfo == None:
#             return None
#         parentInfo = regionInfo
#         while True:
#             if parentInfo.level < level:
#                 return None
#             elif parentInfo.level == level:
#                 return parentInfo
#             else:
#                 parentInfo = self.getParent(parentInfo)
#
#     def getParent(self,regionInfo):
#         if regionInfo == None:
#             return None;
#         return self.getWithRegionCode(regionInfo.getParentRegionCode)
#
#     def getSpec(self,province, l2, l3):
#         provinceInfo = None
#         cityInfo = None
#         countyInfo = None
#         provinceInfo = self.getSpec(province, 1)
#         dianpingL2Info = None
#         dianpingL3Info = None
#         if len(l2) != 0 and len(l3) != 0:
#             dianpingL3Info = getWithParent(l3, l2)
#             dianpingL2Info = self.getParent(dianpingL3Info)
#             if provinceInfo == None:
#                 provinceinfo = self.getParentWithLevel(dianpingL2Info, 1)
#             else:
#                 if province != self.getParentWithLevel(dianpingL2Info, 1):
#                     dianpingL2Info = None
#                     dianpingL3Info = None
#         # 获取dianpingL2Info
#         if dianpingL2Info == None:
#             if provinceinfo != None:
#                 dianpingL2Info = getWithParent(l2, provinceInfo)
#                 if dianpingL2Info == None:
#                     l2 = RegionInfo.fullNameToSimpleName(l2)
#                     dianpingL2Info = getWithParent(l2, provinceinfo)
#             else:
#                 dianpingL2Info = self.getHighest(l2)
#                 if dianpingL2Info == None:
#                     l2 = RegionInfo.fullNameToSimpleName(l2)
#                     dianpingL2Info = self.getHighest(l2)
#                 provinceinfo = self.getParentWithLevel(dianpingL2Info, 1)
#                 if provinceinfo != None:
#                     print provinceinfo
#         if dianpingL2Info != None:
#             if dianpingL2Info.level == 2:
#                 cityInfo = dianpingL2Info
#                 if dianpingL3Info == None:
#                     dianpingL3Info = getWithParent(l3, cityInfo)
#                 countyInfo = self.getParentWithLevel(dianpingL3Info, 3)
#             elif dianpingL2Info.level == 3:
#                 cityInfo = self.getParent(dianpingL2Info)
#                 countyInfo = dianpingL2Info
#         else:
#             print "DianpingL2Info is null. province", province, "l2", l2, "l3", l3
#         regionInfos = [provinceinfo, cityInfo, countyInfo]
#         return regionInfos
#
#     def regionCodeLenTo6(self,srcRegionCode):
#         if len(srcRegionCode) == 0:
#             return srcRegionCode
#         desRegionCode = srcRegionCode
#         if len(srcRegionCode) > 6:
#             desRegionCode = srcRegionCode[0:6]
#         if len(srcRegionCode) < 6:
#             desRegionCode = srcRegionCode
#             len = 6
#             cur = len(srcRegionCode)
#             while cur < len:
#                 desRegionCode = desRegionCode + "0"
#                 cur = cur + 1
#         return desRegionCode
#
#
# class classA:
#     dic={u"address":u"大师的发生"}
#     def __init__(self,name,age):
#         self.name = name
#         self.age = age
#         self.colors = ['red','blue','black']
#
#     @staticmethod
#     def testStatic(aaa):
#         print aaa
#
# if __name__ == '__main__':
#    classA.testStatic(classA.dic)
#    classA.dic[u"phone"]=u'12234445'
#    classA.testStatic(classA.dic)
