#!/usr/bin/env python
# coding=utf-8
import urllib
from GaodeGeoCode import *

def getLogLatByAddress(city, address):
    proxyAddr = "172.17.252.61"
    proxyPort = 8224
    clientType = 1
    useProxy = False;
    getLatLonService = r'http://restapi.amap.com/v3/geocode/geo'
    readtimeout = 3000
    # locationService = "http://172.17.252.61:8224/HLW/Mapbar/MapLocationService/MapLocationServiceProxy"
    # getLatLonService = "http://172.17.252.61:8224/HLW/Mapbar/MapGetLatLonService/MapGetLatLonServiceProxy"
    # busRouteMService = "http://172.17.252.61:8224/HLW/Mapbar/MapBusRouteMService/MapBusRouteMServiceProxy"
    # busRouteWService = "http://172.17.252.61:8224/HLW/Mapbar/MapBusRouteWService/MapBusRouteWServiceProxy"
    # adjustLonlatService = "http://172.17.252.61:8224/HLW/Mapbar/MapAdjustLonlatService/MapAdjustLonlatServiceProxy"
    if clientType == -1 or city == None or address == None:
        print '参数不完整'
        return None

    import sys

    reload(sys)
    sys.setdefaultencoding('utf8')
    urlParam = {
        'city': city.encode('utf-8'),
        'address': address.encode('utf-8')
    }
    getLatLonService = getLatLonService + "?output=xml&key=47edb126ed839b94f834d6abd49f8d81&" + urllib.urlencode(
        urlParam)

    content = urllib.urlopen(getLatLonService)

    return content

def getCoor(content):
    from xml.dom.minidom import parse
    import xml.dom.minidom

    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parseString(content)
    collection = DOMTree.documentElement
    geocodes = collection.getElementsByTagName("geocodes")

    coor = None
    # 打印每部电影的详细信息
    for geocode in geocodes:
        if geocode.getElementsByTagName("location"):
            node = geocode.getElementsByTagName("location")[0]
            data = node.childNodes[0].data
            data = data.split(',')
            coor = [float(data[0]), float(data[1])]
    return coor

def getGaodeGeiCode(content):
    from xml.dom.minidom import parse
    import xml.dom.minidom

    # 使用minidom解析器打开 XML 文档
    DOMTree = xml.dom.minidom.parseString(content)
    collection = DOMTree.documentElement
    geocodes = collection.getElementsByTagName("geocodes")

    coor = None
    district = None
    adcode = None
    for geocode in geocodes:
        if geocode.getElementsByTagName("location"):
            node = geocode.getElementsByTagName("location")[0]
            if len(node.childNodes) != 0:
                data = node.childNodes[0].data
                data = data.split(',')
                coor = [float(data[0]), float(data[1])]
        if geocode.getElementsByTagName("district"):
            node = geocode.getElementsByTagName("district")[0]
            if len(node.childNodes) != 0:
                data = node.childNodes[0].data
                data = data.split(',')
                district = data
        if geocode.getElementsByTagName("adcode"):
            node = geocode.getElementsByTagName("adcode")[0]
            if len(node.childNodes) != 0:
                data = node.childNodes[0].data
                data = data.split(',')
                adcode = data
    return GaodeGeoCode(coor,district,adcode)

def addr2Coor(city,address):
    content = getLogLatByAddress(city,address )
    str2 = str(content.read())
    coor = getCoor(str2)
    if None == coor:
        print "定位失败"
        return None
    return coor

def addr2coorAndCode(city,address):
    content = getLogLatByAddress(city, address)
    str2 = str(content.read())
    gaodeGeoCode = getGaodeGeiCode(str2)
    if None == gaodeGeoCode:
        print "定位失败"
        return None
    return gaodeGeoCode


if __name__ == '__main__':
    gaodeGeoCode =  addr2coorAndCode(u'长春市',u'吉林省长春市朝阳区重庆路万达广场1楼味道面包坊')
    print gaodeGeoCode.adcode,gaodeGeoCode.district,gaodeGeoCode.lonLat