#!/usr/bin/env python
#coding:utf-8



brand_dic={}

brand_dic['你好']={'name':'你好','brandId':1,'category':'丽人','subCategory':'理发'}
brand_dic['你好']={'name':'你好','brandId':1,'category':'丽人','subCategory':'理发'}
brand_dic['好好']={'name':'好好','brandId':1,'category':'丽人','subCategory':'理发'}

for brand in brand_dic:
    if brand_dic.get(brand)!=None:
        print brand_dic.get(brand)

if brand_dic.get('好好好') == None:
    brand_dic['好好好']=1

for brand in brand_dic:
    if brand_dic.get(brand)!=None:
        print brand_dic.get(brand)