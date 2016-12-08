#!/usr/bin/env python
# coding:utf-8
import re
import datetime
# {weekDays:[1,2,3,4,5],start:1970-01-01 08:00:00,end:1970-01-01 14:00:00}＃
# {weekDays:[1,2,3,4,5],start:1970-01-01 08:00:00,end:1970-01-01 14:00:00}＃
def scan(timeStr):
    result = u''
    i=0
    while i<len(timeStr)-1:
        if timeStr[i]==u':' or timeStr[i]==u'：':
            j=i+1
            while j<len(timeStr):
                if timeStr[j]==u':' or timeStr[j]==u'：':
                    j =j+1
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

    hPattern = [u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9', u'01', u'02', u'03', u'04', u'05', u'06', u'07',
                u'08', u'09', u'10', u'11', u'12', u'13',
                u'14', u'15', u'16', u'17', u'18', u'19', u'20', u'21', u'22', u'23', u'00']

    mPattern = [u'30', u'00', u'15', u'45']
    dic = {}
    dic[u'1'] = u'01'
    dic[u'2'] = u'0'
    dic[u'3'] = u'03'
    dic[u'4'] = u'04'
    dic[u'5'] = u'05'
    dic[u'6'] = u'06'
    dic[u'7'] = u'07'
    dic[u'8'] = u'08'
    dic[u'9'] = u'09'

    dSeperator = [u'-', u'~', u'—', u'至', u'至', u'-', u'到']
    tSeperator = [u':', u'：', u'.',u'。']

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
    if timeStr.find(u'周末'):
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

        openhours.append(
            {"weekDays": weekDays,
             "start": datetime.datetime(1970, 01, 01, int(timeList[0])%24, int(timeList[1])%60, 00),
             "end": datetime.datetime(1970, 01, 01, int(timeList[2])%24, int(timeList[3])%60, 00)})
    return openhours
def getOpenHour(timeStr):
    try:
        weekDays, weekDaystmp, timeList = timeExtract(timeStr)
        return parseTime(weekDays, weekDaystmp, timeList)
    except Exception, e:
        print e, "Exception"
    return
if __name__ == '__main__':
    timeStr = u'周一至周五：10:00:::00-22:00:00；周末：10:00:00-22:::：：：:30:00'

    print  getOpenHour(timeStr)
