#!/usr/bin/env python
#coding:utf-8

import sys

reload(sys)

sys.setdefaultencoding('utf8')
from utils import *

def contain_chinese(str):
    str = unicode(str)
    for ch in str:
        if is_chinese(ch):
            return True
    return False

def remove_special_ch(str):
    str = unicode(str)
    newLine = u''
    for ch in str:
        if is_chinese(ch) or is_alphabet(ch):
            newLine = newLine+ch


    return newLine.upper()
if __name__ == "__main__":
    fi = open('/Users/YHQ/Downloads/unionpayshop/head.txt', 'rb')
    fo = open('/Users/YHQ/Downloads/unionpayshop/head_.txt', 'wb')

    for line in fi:
        newline = remove_special_ch(line)+'\n'

        if len(newline) ==0 or  newline==u'\n':
            continue;

        fo.write(newline.encode('utf-8'))
    fo.close()
    fi.close()