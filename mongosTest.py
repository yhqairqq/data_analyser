#!/usr/bin/env python
#coding:utf-8
import os
import fnmatch
import json
import time
import pymongo
import datetime
import traceback


conn = pymongo.MongoClient('mysql1.cuone.com',27017)


