#!/usr/bin/env python
# coding=utf-8
import pymongo
import datetime
from bson.objectid import ObjectId
import sys

sys.path.append("..")
from gaode.MapService import *
from code2Name.App import *


def updateAddressInfoAndLonlat(db, regionContainer):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = db.MainShop5.find(
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop5.find(
    ).sort('_id', pymongo.ASCENDING).count()

    print 'totalSize:', count

    if count == 0:
        exit(1)

    while True:
        row = 0
        for json in content:
            row = row + 1
            if row == page_size - 1:
                last_row_id = json[u'_id']
            i = i + 1
            if i % 10000 == 0:
                print "完成>>>>%.2f" % (i / count * 100), "%"
            try:
                address = json[u'address']
                citycode = json[u'city']
                shopName = json[u'shopName']
                addressInfo_address = json[u'addressInfo'][u'address']
                addressInfo_addrProvince = json[u'addressInfo'][u'addrProvince']
                addressInfo_addrCity = json[u'addressInfo'][u'addrCity']
                addressInfo_addrCounty = json[u'addressInfo'][u'addrCounty']
                flag = 1
                if citycode == None or citycode == 0:
                    continue

                citycode = str(citycode)
                pro, city, county = regionContainer.getProCityCountyWithRegionCode(citycode)
                # print pro, city, county

                if pro != None:
                    addressInfo_addrProvince = pro
                if county != None and len(addressInfo_addrCounty) == 0:
                    addressInfo_addrCounty = county

                if city == None:
                    city = addressInfo_addrCity

                gaodeGeoCode = addr2coorAndCode(city, address)
                if gaodeGeoCode == None:
                    gaodeGeoCode = addr2coorAndCode(city, shopName)
                # print gaodeGeoCode.adcode, gaodeGeoCode.district, gaodeGeoCode.lonLat
                if gaodeGeoCode == None:
                    date_time = datetime.datetime.utcnow()
                    result = db.MainShop5.update_one({'_id': json[u'_id']}, {
                        '$set': {'addressInfo.addrProvince': pro, 'addressInfo.addrCountry': addressInfo_addrCounty,
                                 'flag': flag, "updateAt": date_time}}, True)
                    if result.matched_count > 0:
                        if i % 1000 == 0:
                            print '更新成功', json[u'_id']
                    continue

                if len(addressInfo_addrCounty) == 0 and gaodeGeoCode.district != None:
                    addressInfo_addrCounty = gaodeGeoCode.district

                coordiate = gaodeGeoCode.lonLat

                date_time = datetime.datetime.utcnow()
                result = db.MainShop5.update_one({'_id': json[u'_id']}, {
                    '$set': {'addressInfo.addrProvince': pro, 'addressInfo.addrCountry': addressInfo_addrCounty,
                             'coordinates': coordiate,
                             'addressInfo.coordinates': coordiate,
                             'flag': flag, "updateAt": date_time}}, True)
                if result.matched_count > 0:
                    if i % 1000 == 0:
                        print '更新成功', json[u'_id']

            except Exception, e:
                print e, "Exception", json[u'_id']

        if last_row_id != '':
            content = db.MainShop5.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)}
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            exit(1);


if __name__ == '__main__':
    # conn = pymongo.MongoClient('127.0.0.1', 33332)
    conn = pymongo.MongoClient('10.15.159.169', 30000)
    import sys, os

    path = sys.path[0]
    path = path[0:path.rindex('/')] + '/code2Name/county_region_2015.dic'
    regionContainer = getRegionContainer(path)

    # # 连接数据库
    db = conn.crawl_hz
    updateAddressInfoAndLonlat(db, regionContainer)

    # import sys, os
    # path =   sys.path[0]
    # path = path[0:path.rindex('/')]+'/code2Name/county_region_2015.dic'
    # print path


    # gaodeGeoCode = addr2coorAndCode('长春市', '吉林省长春市朝阳区重庆路万达广场1楼味道面包坊')
    # print gaodeGeoCode.adcode, gaodeGeoCode.district, gaodeGeoCode.lonLat
    # # regionContainer = getRegionContainer('/Users/YHQ/python_pro/untitled/code2Name/county_region_2015.dic')
    # fullCode = '220104'
    # pro, city, county = regionContainer.getProCityCountyWithRegionCode(fullCode)
    # print pro, city, county
