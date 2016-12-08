#!/usr/bin/python
# -*- coding:utf8 -*-

import os
import fnmatch
import  json
allFileNum = 0
def getTargetFileList(regex, path,dst):
    global allFileNum
    '''
    打印一个目录下的所有文件夹和文件
    '''
    # 所有文件
    fileList = []
    dstFileList = []
    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    for f in files:
        if(os.path.isfile(path + '/' + f) and fnmatch.fnmatch(f,regex)):
            # 添加文件
            fileList.append(path + '/' + f)
    dstfiles = os.listdir(dst)
    for df in dstfiles:
        if(os.path.isfile(dst + '/' + df) and fnmatch.fnmatch(df,regex)):
            # 添加文件
            dstFileList.append(dst + '/' + df)
    return fileList,dstFileList

def fileIsExist(src,dstList):
    for dst in dstList:
        dstName=dst[dst.rfind('/'):]
        srcName=src[src.rfind('/'):]
        if(dstName  == srcName):
            return 1

    return -1

def processFileList(fileList,dstFileList,fieldsArray):
    for f in fileList:

        if(fileIsExist(f,dstFileList) > 0):
            continue

        new_file = f[0:f.rfind('/')]+'/copy'+f[f.rfind('/'):]
        fi = open(f,'rb')
        fo = open(new_file,'w')

        print 'start process:'+f
        for line in fi.readlines():


            if len(line.split(':')) < 3:
                fo.writelines(line)
                continue
            jline=json.loads(line,encoding='UTF-8')
            for key in fieldsArray.keys():
                if(key == 'addressInfo'):
                    if(jline[key] == None):
                        data = {'address':'','addrCountry':'','addrProvince':'','addrCity':'','addrCounty':'','addrTown':'','addrRoad':'','addrHouseNo':'','addrBuilding':'','addrDetail':''}

                        strData = json.dumps(data)

                        jdata = json.loads(strData,'utf-8')

                        jline[key]= jdata
                    else:
                        for sub in fieldsArray[key].keys():
                           if(jline[key][sub] == None):
                                if(fieldsArray[key][sub] == 'string'):
                                  jline[key][sub]=''
                                if(fieldsArray[key][sub] == 'list'):
                                  jline[key][sub]=[]
                else:
                    if(jline[key] == None):
                      if(fieldsArray[key] == 'string'):
                          jline[key] = ''
                      if(fieldsArray[key] == 'list'):
                         jline[key] = []

            data_string = json.dumps(jline, 'utf8')
            data_string = data_string.encode('utf8')
            fo.writelines(data_string)
        fi.close()
        fo.close()
        print 'finish  .  . . '

if __name__ == '__main__':
   #fileList=getTargetFileList('*.json', '/Users/YHQ/workspace/zoo/butterfly/target/test-classes/json')
   fileList,dstFileList=getTargetFileList('*.json', '/Users/YHQ/workspace/zoo/butterfly/target/test-classes/json','/Users/YHQ/workspace/zoo/butterfly/target/test-classes/json/copy')
   dicField = {'dataOrigin':'string','shopName':'string','shopId':'string','category':'list','subCategory':'list','logo':'string','telephones':'list','tradingArea':'string','pictureList':'list','tags':'list','openingHours':'list','addressInfo':{'address':'string','addrCountry':'string','addrProvince':'string','addrCity':'string','addrCounty':'string','addrTown':'string','addrRoad':'string','addrHouseNo':'string','addrBuilding':'string','addrDetail':'string'}}

   processFileList(fileList,dstFileList,dicField)