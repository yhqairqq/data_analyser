#!/usr/bin/env Python
# -*- coding:utf-8 -*-
import math
# """汉字处理的工具:
# 判断unicode是否是汉字，数字，英文，或者其他字符。
# 全角符号转半角符号。"""

# __author__="internetsweeper <zhengbin0713@gmail.com>"
# __date__="2007-08-04"

import re


def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """判断是否非汉字，数字和英文字符"""
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
        return True
    else:
        return False


def B2Q(uchar):
    """半角转全角"""
    inside_code = ord(uchar)
    if inside_code < 0x0020 or inside_code > 0x7e:  # 不是半角字符就返回原来的字符
        return uchar
    if inside_code == 0x0020:  # 除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code = 0x3000
    else:
        inside_code += 0xfee0
    return unichr(inside_code)


def Q2B(uchar):
    """全角转半角"""
    inside_code = ord(uchar)
    if inside_code == 0x3000:
        inside_code = 0x0020
    else:
        inside_code -= 0xfee0
    if inside_code < 0x0020 or inside_code > 0x7e:  # 转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)


def stringQ2B(ustring):
    """把字符串全角转半角"""
    return "".join([Q2B(uchar) for uchar in ustring])


def uniform(ustring):
    """格式化字符串，完成全角转半角，大写转小写的工作"""
    return stringQ2B(ustring).lower()


def string2List(ustring):
    """将ustring按照中文，字母，数字分开"""
    retList = []
    utmp = []
    for uchar in ustring:
        if is_other(uchar):
            if len(utmp) == 0:
                continue
            else:
                retList.append("".join(utmp))
                utmp = []
        else:
            utmp.append(uchar)
    if len(utmp) != 0:
        retList.append("".join(utmp))
    return retList


def check_contain_chinese(check_str):
    try:
        for ch in check_str:
            ch = unicode(ch)
            if u'\u4e00' <= ch <= u'\u9fff':
                return True
        return False
    except Exception, e:
        print 'check_contain_chinese in', e


def check_contain_english(uchar_str):
    try:
        for uchar in uchar_str:
            uchar = unicode(uchar)
            if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
                return True
        return False
    except Exception, e:
        print 'check_contain_english in', e


def check_contain_digital(uchar_str):
    try:
        for uchar in uchar_str:
            uchar = unicode(uchar)
            if uchar >= u'\u0030' and uchar <= u'\u0039':
                return True
        return False
    except Exception, e:
        print 'check_contain_digital in', e


def getGDDistance(p1, p2):
    lon1 = math.pi / 180 * p1[0]  # 经
    lon2 = math.pi / 180 * p2[0]  # 纬
    lat1 = math.pi / 180 * p1[1]
    lat2 = math.pi / 180 * p2[1]
    # 地球半径
    R = 6371
    d = math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(lon2 - lon1)) * R
    return d


def remove_ch(str):
    str = re.sub(u' ', '', str)
    str = re.sub(u'…', '', str)
    # str = re.sub(u'.', '', str)
    str = re.sub(u'。', '', str)
    str = re.sub(u',', '', str)
    str = re.sub(u'…', '', str)
    str = re.sub(u'＞', '', str)
    str = re.sub(u'@', '', str)
    str = re.sub(u'/', '', str)
    str = re.sub(u'-', '', str)
    str = re.sub(u'_', '', str)
    str = re.sub(u'#', '', str)
    str = re.sub(u'﹉', '', str)
    str = re.sub(u';', '', str)
    str = re.sub(u'、', '', str)
    str = re.sub(u'】', '', str)
    str = re.sub(u'%', '', str)
    str = re.sub(u'\+', '', str)
    str = re.sub(u'`', '', str)
    str = re.sub(u'、', '', str)
    str = re.sub(u'\?', '', str)
    str = re.sub(u'|', '', str)
    str = re.sub(u'！', '', str)
    str = re.sub(u'，', '', str)
    str = re.sub(u'～', '', str)
    str = re.sub(u'—', '', str)
    str = re.sub(u'。', '', str)
    str = re.sub(u'’', '', str)
    str = re.sub(u'‘', '', str)
    str = re.sub(u'\*', '', str)
    str = re.sub(u'（', '', str)
    str = re.sub(u'&', '', str)
    str = re.sub(u'》', '', str)
    str = re.sub(u'《', '', str)
    str = re.sub(u'~', '', str)
    str = re.sub(u'!', '', str)
    str = re.sub(u'\{', '', str)
    str = re.sub(u'\}', '', str)
    str = re.sub(u'\(', '', str)
    str = re.sub(u'\)', '', str)
    return str


if __name__ == "__main__":
    # str_utf8 = unicode('!!!a你好{}（）90()1!!!', 'utf-8')
    # print str_utf8
    # print check_contain_english(str_utf8)
    # print check_contain_chinese(str_utf8)
    # print check_contain_digital(str_utf8)

    demo = u'你好~!@#$%^&*()_+?><你好":{}][|?/'
    new =u''
    for ch in demo:
        if is_other(ch)==False:
             new = new +ch

    print new


#  p1 = [120.109148,30.281882]
#  p2 = [120.114105,30.282039]
#
#  print getGDDistance(p1,p2)
