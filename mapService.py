# -*- coding: utf-8 -*-
#encoding=utf-8

import urllib2
import sys, json
from StringIO import StringIO

send_headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, sdch',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Host':'restapi.amap.com',
        'Referer':'http://lbs.amap.com/fn/iframe/?id=3556',
}

def getDataWithEx(url):
    req = urllib2.Request(url,headers=send_headers)
    r = urllib2.urlopen(req,timeout=30)

    # if r.info().get('Content-Encoding') == 'gzip':
    #     buf = StringIO(r.read())
    #     f = gzip.GzipFile(fileobj=buf)
    #     data = f.read()
    # else:
    #     data = r.read()
    # return json.loads(data[13:-1])
    data =r.read()
    return data
def getData(url):
    while 1:
        try:
            response = getDataWithEx(url)
            break
        except Exception, e:
            print 'retry:' + url + " with error " + str(e)
    return response

map_url = r'http://restapi.amap.com/v3/place/text?key=74657a8c71440f4676bc7de55cbe8f41&keywords=安松街67号&types=&city=哈尔滨&children=1&offset=20&page=1&extensions=all'

req = urllib2.Request(map_url)
r = urllib2.urlopen(req,timeout=30)

# if r.info().get('Content-Encoding') == 'gzip':
#     buf = StringIO(r.read())
#     f = gzip.GzipFile(fileobj=buf)
#     data = f.read()
# else:
#     data = r.read()
# return json.loads(data[13:-1])
data =r.read()
print data
json = json.loads(data)
for poi in json[u'pois']:
    print poi[u'location']