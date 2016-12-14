#!/usr/bin/env python
# coding=utf-8

from RegionInfo import *
from RegionContainer import *

def getRegionContainer(path):
    RegionInfo.initLevelLen()
    RegionInfo.initCache()

    regionContainer = RegionContainer(path)

    regionContainer.load()
    return  regionContainer

if __name__ == '__main__':

    # RegionInfo.initLevelLen()
    # RegionInfo.initCache()
    #
    # regionContainer = RegionContainer('/Users/YHQ/python_pro/untitled/code2Name/county_region_2015.dic')
    #
    # regionContainer.load()

    regionContainer = getRegionContainer('/Users/YHQ/python_pro/untitled/code2Name/county_region_2015.dic')

    fullCode = '220104'
    # shortProvinceCode = fullCode[0:2]
    # shortCityCode = fullCode[0:4]
    # shortCountyCode = fullCode
    #
    # regionInfo = regionContainer.getWithRegionCode(shortProvinceCode)
    # if regionInfo!=None:
    #     print 'province',regionInfo.fullName
    # regionInfo = regionContainer.getWithRegionCode(shortCityCode)
    # if regionInfo != None:
    #     print 'city', regionInfo.fullName
    # regionInfo = regionContainer.getWithRegionCode(shortCountyCode)
    # if regionInfo!=None:
    #     print 'county',regionInfo.fullName

    pro,city,county =  regionContainer.getProCityCountyWithRegionCode(fullCode)
    print pro,city,county
    # regionContainerFull = RegionContainer('/Users/YHQ/python_pro/untitled/code2Name/region.dic')
    #
    # regionContainerFull.load()


