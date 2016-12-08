#!/usr/bin/env python
# coding:utf-8
#将品牌表中的子分类,改为其他
import pymongo
from bson.objectid import ObjectId
from utils import *
def remove_other(str):
    new =u''
    if str == None:
        new
    for ch  in str:
        if is_other(ch)==False:
            new = new+ch
    return  new

def isValid(shopName):

    invalidItem = {u"商户", u"信用卡", u"银联", u"纪念", u"专场", u"扫码", u"约惠", u"活动", u"银行", u"随机", u"立减", u"银行"};

    for item in invalidItem:
        if item==u"银行" and shopName.find(item) != -1 and len(shopName) == 4:
            return True
        if shopName.find(item) != -1:
            return False
    return True


def updateUnionPayShop(db):
    page_size = 10000
    i = 1.0
    last_row_id = ''
    content = db.MainShop_DataOrigin_Unionpay.find(
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop_DataOrigin_Unionpay.find(
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

                shop_name = json[u'shopName']
                address = json[u'address']
                address = remove_other(address)
                if isValid(shop_name) == False or address == u'' or address == None:
                    _id = json[u'_id']
                    result = db.MainShop_DataOrigin_Unionpay.delete_one({u'_id': ObjectId(_id)})
                    if result.deleted_count > 0:
                        if i%1000==0:
                          print '删除',json[u'_id']

            except Exception, e:
                if e == u'address':
                    _id = json[u'_id']
                    result = db.MainShop_DataOrigin_Unionpay.delete_one({u'_id': ObjectId(_id)})
                    if result.deleted_count > 0:
                        if i % 1000 == 0:
                            print '删除', json[u'_id']
                    result = db.MainShop_DataOrigin_Unionpay.delete_one({u'_id': ObjectId(_id)})
                print e, "Exception",json[u'_id']

        if last_row_id != '':
            content = db.MainShop_DataOrigin_Unionpay.find(
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
    # # 连接数据库
    db = conn.crawl_hz
    # updateUnionPayShop(db)

    # timeStr = u'800---22:00'
    # # print deepExtractTimeList(timeStr)
    # print  getOpenHour(timeStr)
    #  str = u"1233你好"
    #  print str.find(u'你好')

    shopName = u'asfasdf随机123+_(*&^'
    print isValid(shopName)
    print remove_other(shopName)