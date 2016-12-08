#!/usr/bin/env python
# coding:utf-8
import os
import fnmatch
import json
import time
import pymongo
import datetime
import traceback

allFileNum = 0
# conn = pymongo.MongoClient('mysql1.cuone.com',27017)
# conn = pymongo.MongoClient('mongodb://root:unionpay201607@10.15.151.81:27017/')
conn = pymongo.MongoClient('127.0.0.1', 33333)
# conn = pymongo.MongoClient('10.15.86.90',30000)
fi = open('/Users/YHQ/baiduyun/dianping.csv', 'rb')
db = conn.crawl

# value_pattern = {'shop_id': '', 'mall_id': '', 'verified': '', 'is_closed': '', 'name': '', 'alias': '', 'province': '',
#                  'city': '', 'city_pinyin': '', 'city_id': '', 'area': '', 'big_cate': '', 'big_cate_id': '',
#                  'small_cate': '', 'small_cate_id': '', 'address': '', 'business_area': '', 'phone': '', 'hours': '',
#                  'avg_price': '', 'stars': '', 'photos': '', 'description': '', 'tags': '', 'map_type': '',
#                  'latitude': '', 'longitude': '', 'navigation': '', 'traffic': '', 'parking': '', 'characteristics': '',
#                  'product_rating': '', 'environment_rating': '', 'service_rating': '', 'default_remarks': '',
#                  'all_remarks': '', 'very_good_remarks': '',
#                  'good_remarks': '', 'common_remarks': '', 'bad_remarks': '', 'very_bad_remarks': '',
#                  'good_summary': '', 'bad_summary': '', 'recommended_dishes': '',
#                  'recommended_products': '', 'nearby_shops': '', 'is_chains': '', 'take_away': '', 'tuan': '',
#                  'card': '', 'history': '', 'latest_comment_date': '', 'visits_total': '', 'visits_month': '',
#                  'visits_week': '', 'num_collected': ''}

total = 22560925.0
count = 0
in_start = 0.0
line = fi.readline()

while line != None and line != "":
    count = count + 1
    try:
        values = line.split('##')
        if count%1000==0:
            print len(values)

        if len(values) != 56:
            continue

        date_time = datetime.datetime.utcnow()
        # 假如处理的方法
        result = db.dianping_origindata.insert_one(
            {'shop_id': values[0], 'mall_id': values[1], 'verified': values[2], 'is_closed': values[3],
             'name': values[4],
             'alias': values[5], 'province': values[6],
             'city': values[7], 'city_pinyin': values[8], 'city_id': values[9], 'area': values[10],
             'big_cate': values[11], 'big_cate_id': values[12],
             'small_cate': values[13], 'small_cate_id': values[14], 'address': values[15], 'business_area': values[16],
             'phone': values[17], 'hours': values[18],
             'avg_price': values[19], 'stars': values[20], 'photos': values[21], 'description': values[22],
             'tags': values[23], 'map_type': values[24],
             'latitude': values[25], 'longitude': values[26], 'navigation': values[27], 'traffic': values[28],
             'parking': values[29], 'characteristics': values[30],
             'product_rating': values[31], 'environment_rating': values[32], 'service_rating': values[33],
             'default_remarks': values[34],
             'all_remarks': values[35], 'very_good_remarks': values[36],
             'good_remarks': values[37], 'common_remarks': values[38], 'bad_remarks': values[39],
             'very_bad_remarks': values[40],
             'good_summary': values[41], 'bad_summary': values[42], 'recommended_dishes': values[43],
             'recommended_products': values[44], 'nearby_shops': values[45], 'is_chains': values[46],
             'take_away': values[47], 'tuan': values[48],
             'card': values[49], 'history': values[50], 'latest_comment_date': values[51], 'visits_total': values[52],
             'visits_month': values[53],
             'visits_week': values[54], 'num_collected': values[55], 'createAt': date_time, 'updateAt': date_time})
        if result.inserted_id != None and count % 10000 == 0:
            print '更新成功>>>>>>', result.inserted_id
        if count % 10000 == 0:
            print "完成>>>>%.2f" % (count / total * 100), "%"
    except Exception, e:
        print '异常处理完成>>>>',e

    line = fi.readline()
fi.close()
print 'finish  .  . . '
