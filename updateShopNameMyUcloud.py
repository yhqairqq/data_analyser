#!/usr/bin/env python
# coding:utf-8
#将品牌表中的子分类,改为其他
import pymongo
import datetime
from bson.objectid import ObjectId


def scan(timeStr):

    result = u''
    i=0
    while i<len(timeStr)-1:
        if timeStr[i]==u':' or timeStr[i]==u'：' or timeStr[i]==u';':
            j=i+1
            while j<len(timeStr):
                if timeStr[j]==u':' or timeStr[j]==u'：' or timeStr[j]==u';':
                    j =j+1
                    if j == len(timeStr):
                        i=j-1
                else:
                    result = result+timeStr[i]
                    i=j
                    break
        else:
            result = result+timeStr[i]
            i = i+1

    result=result+timeStr[i]
    return result


def isH(h, tSeperator, str, startIndex):
    for sep in tSeperator:
        # print str[startIndex:startIndex + len(h)+1]
        subStr = str[startIndex:startIndex + len(h) + 1]
        if subStr.find(sep) != -1:
            return True
    return False
def isNum(c):
    if c >= u'0' and c <= u'9':
        return True
    return False


def timeExtract(timeStr):
    timeStr = scan(timeStr)

    weekDays = []
    weekDaystmp = []
    timeList = []

    if len(timeStr) == 0 or timeStr == None:
        return
    # timeStr = u'周一到周五8:00-19:00 周六到周日 9:00-22:00'
    # timeStr = u'10：00－22：00'
    wKeys = [u'每天', u'每晚']

    weekDaysPattern = [u'周一', u'周二', u'周三', u'周四', u'周五', u'周六', u'周日']

    hPattern = [u'0',u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'01', u'02', u'03', u'04', u'05', u'06', u'07',
                u'08', u'09', u'10', u'11', u'12', u'13',
                u'14', u'15', u'16', u'17', u'18', u'19', u'20', u'21', u'22', u'23', u'00']

    mPattern = [u'30', u'00', u'15', u'45']
    dic = {}
    dic[u'0'] = u'00'
    dic[u'1'] = u'01'
    dic[u'2'] = u'02'
    dic[u'3'] = u'03'
    dic[u'4'] = u'04'
    dic[u'5'] = u'05'
    dic[u'6'] = u'06'
    dic[u'7'] = u'07'
    dic[u'8'] = u'08'
    dic[u'9'] = u'09'

    dSeperator = [u'-', u'~', u'—', u'至', u'至', u'-', u'到']
    tSeperator = [u':', u'：', u'.',u'。',u';',u'；']

    if timeStr.find(u'无') != -1 and timeStr.find(u'时间') != -1:
        return weekDays, weekDaystmp, timeList

    # 首先查看是否存在全覆盖关键词，只要找到一个停止便利，将weekdays设置为[1,2,3,4,5,6,7]
    lindex = -1
    for key in wKeys:
        lindex = timeStr.find(key)
        if lindex != -1:
            weekDays = [1, 2, 3, 4, 5, 6, 7]
            break

    # 其次检查是否存在周几到关键词,如果一个都没有，侧默认为是周一到周日

    lindex = -1
    weekDaystmp = []
    for i in range(len(weekDaysPattern)):
        lindex = timeStr.find(weekDaysPattern[i])
        if lindex != -1:
            weekDaystmp.append(i + 1)
    if timeStr.find(u'周末')!=-1:
        weekDaystmp.append(6)
        weekDaystmp.append(7)

    # 检查时间区间
    startIndex = 0
    while startIndex < len(timeStr):
        c = timeStr[startIndex:startIndex + 1]
        if isNum(c):
            if isH(c, tSeperator, timeStr, startIndex):
                timeList.append(dic.get(c))
                startIndex = startIndex + len(c) + 1
                c = timeStr[startIndex:startIndex + 2]
                timeList.append(c)
                startIndex = startIndex + len(c) + 1
            else:
                c = timeStr[startIndex:startIndex + 2]
                if isH(c, tSeperator, timeStr, startIndex):
                    timeList.append(c)
                    startIndex = startIndex + len(c) + 1
                    c = timeStr[startIndex:startIndex + 2]
                    timeList.append(c)
                    startIndex = startIndex + len(c) + 1
                else:
                    startIndex = startIndex+ len(c)
        else:
            startIndex = startIndex + 1
    return weekDays, weekDaystmp, timeList

def deepExtractTimeList(timeStr):
    timeList=[]
    i=0

    while i<len(timeStr):
        j = i
        c=timeStr[i]
        if isNum(c):
            while j<len(timeStr):
                if isNum(timeStr[j]):
                    j=j+1
                else:
                    break
            subStr=timeStr[i:j]
            if len(subStr)%2==0:
                for i in range(0,len(subStr)/2,1):
                    timeList.append(subStr[0+i*2:2+i*2])
            if len(subStr)==1:
                timeList.append(subStr)
            if len(subStr)==3:
                timeList.append(subStr[0:1])
                timeList.append(subStr[1:3])
            if len(subStr) == 5:
                timeList.append(subStr[0:1])
                timeList.append(subStr[1:3])
                j = j-2
            i=j
        else:
            i = i+1
    return timeList

def parseTime(weekDays, weekDaystmp, timeList):
    # y, M, d, h, m, s = 2016, 10, 01, 00, 00, 0
    # d = datetime.datetime(y, M, d, h, m, s)
    # 1970 - 01 - 01
    openhours = []
    if len(weekDays) == 0 and len(weekDaystmp) == 0 and len(timeList) == 0:
        return

    if len(weekDays) != 0:
        if len(timeList) == 0:
            openhours.append({"weekDays": weekDays, "start": datetime.datetime(1970, 01, 01, 00, 00, 00),
                              "end": datetime.datetime(1970, 01, 01, 23, 00, 00)})
        else:
            if len(timeList) == 4:
                openhours.append(
                    {"weekDays": weekDays,
                     "start": datetime.datetime(1970, 01, 01, int(timeList[0])%24, int(timeList[1])%60, 00),
                     "end": datetime.datetime(1970, 01, 01, int(timeList[2])%24, int(timeList[3])%60, 00)})
    if len(weekDaystmp) != 0:
        if len(weekDaystmp) == 2:
            for i in range(weekDaystmp[0], weekDaystmp[1] + 1, 1):
                weekDays.append(i)
            if len(timeList) == 0:
                openhours.append({"weekDays": weekDays, "start": datetime.datetime(1970, 01, 01, 00, 00, 00),
                                  "end": datetime.datetime(1970, 01, 01, 23, 00, 00)})
            else:
                openhours.append(
                    {"weekDays": weekDays,
                     "start": datetime.datetime(1970, 01, 01, int(timeList[0])%24, int(timeList[1])%60, 00),
                     "end": datetime.datetime(1970, 01, 01, int(timeList[2])%24, int(timeList[3])%60, 00)})
        else:
            if len(weekDaystmp) == 4:
                for i in range(0, 4, 2):
                    weekDays=[]
                    for j in range(weekDaystmp[i], weekDaystmp[i+1]+1, 1):
                        weekDays.append(j)
                    if len(timeList) == 0:
                        openhours.append({"weekDays": weekDays, "start": datetime.datetime(1970, 01, 01, 00, 00, 00),
                                          "end": datetime.datetime(1970, 01, 01, 23, 00, 00)})
                    else:
                        if len(timeList) == 4:
                            openhours.append(
                                {"weekDays": weekDays,
                                 "start": datetime.datetime(1970, 01, 01, int(timeList[0])%24, int(timeList[1])%60, 00),
                                 "end": datetime.datetime(1970, 01, 01, int(timeList[2])%24, int(timeList[3])%60, 00)})
                        else:
                            if len(timeList) == 8:
                                openhours.append(
                                    {"weekDays": weekDays,
                                     "start": datetime.datetime(1970, 01, 01, int(timeList[0 + 2 * i])%24,
                                                                int(timeList[1 + 2 * i])%60,
                                                                00),
                                     "end": datetime.datetime(1970, 01, 01, int(timeList[2 + 2 * i])%24,
                                                              int(timeList[3 + 2 * i])%60,
                                                              00)})
    if len(weekDays) == 0 and len(weekDaystmp) == 0 and len(timeList) != 0:
        for i in range(1, 8, 1):
            weekDays.append(i)
        if len(timeList)==8:
            count = 0
            while count<2:
                openhours.append(
                    {"weekDays": weekDays,
                     "start": datetime.datetime(1970, 01, 01, int(timeList[0+count*4]) % 24, int(timeList[1+count*4]) % 60, 00),
                     "end": datetime.datetime(1970, 01, 01, int(timeList[2+count*4]) % 24, int(timeList[3+count*4]) % 60, 00)})
                count = count+1
        else:
            openhours.append(
                {"weekDays": weekDays,
                 "start": datetime.datetime(1970, 01, 01, int(timeList[0])%24, int(timeList[1])%60, 00),
                 "end": datetime.datetime(1970, 01, 01, int(timeList[2])%24, int(timeList[3])%60, 00)})
    return openhours
def getOpenHour(timeStr):
    try:
        weekDays, weekDaystmp, timeList = timeExtract(timeStr)

        if len(timeList)%4!=0:
            timeList = deepExtractTimeList(timeStr)

        return parseTime(weekDays, weekDaystmp, timeList)
    except Exception, e:
        print e, "Exception",timeStr
    return

def updateShopName(db):
    page_size = 1000
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
                shop_name_copy = shop_name.strip()

                if(len(shop_name) == len(shop_name_copy)):
                    continue;
                result = db.MainShop_DataOrigin_Unionpay.update_one({'_id':json[u'_id']},{'$set':{"shopName":shop_name_copy}},True)
                if result.matched_count > 0:
                    if i%1000==0:
                      print '更新成功',json[u'_id']

            except Exception, e:
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
    # 连接数据库
    db = conn.crawl_hz
    updateShopName(db)

    # timeStr = u'800---22:00'
    # # print deepExtractTimeList(timeStr)
    # print  getOpenHour(timeStr)