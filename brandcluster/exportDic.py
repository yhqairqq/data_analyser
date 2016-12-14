#!/usr/bin/env python
# coding=utf-8
#导出词典
import pymongo
from bson.objectid import ObjectId
import codecs
def exportDic(db):

    fo = codecs.open("word.dic",'w','utf-8')
    lines=[]

    page_size = 1000
    i = 1.0
    last_row_id = ''
    content = db.MainShop3.find(
    ).sort('_id', pymongo.ASCENDING).limit(page_size)
    count = db.MainShop3.find(
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

                ss = json[u'_1']+u' '+str(json[u'_2'])+'\n'
                lines.append(ss)

            except Exception, e:
                print e, "Exception",json[u'_id']

        if last_row_id != '':
            content = db.MainShop3.find(
                filter={
                    '_id': {'$gt': ObjectId(last_row_id)}
                    # 任意元素匹配所有条件
                }
            ).sort('_id', pymongo.ASCENDING).limit(page_size)
            last_row_id = ''
        else:
            print "完成>>>>%.2f" % (i / count * 100), "%"
            break

    fo.writelines(lines)
    fo.close()


if __name__ == '__main__':
    conn = pymongo.MongoClient('127.0.0.1', 33333)
    # conn = pymongo.MongoClient('10.15.159.169', 30000)
    # 连接数据库
    db = conn.crawl
    exportDic(db)

    # timeStr = u'800---22:00'
    # # print deepExtractTimeList(timeStr)
    # print  getOpenHour(timeStr)