#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-09 11:14:43
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-09 11:56:51
import os
import time

bug_data_path = '/opt/smmc/apk_parse/entire_apk_report_run/data/'
origin_path = '/opt/smmc/apk_parse/hn_data/'
apk_path = '/opt/smmc/data_backup/apk/'

def get_datetime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def update(file_name):
    out = 'cat ' + bug_data_path + file_name + ' > ' + origin_path + file_name
    os.system(out)

def update_all():
    update('log.txt')
    update('md5.txt')
    update('problem_apk.txt')

def push_origin():
    add = 'git add --all'
    commit = 'git commit -m ' + get_datetime()
    push = 'git push origin master'
    os.system('cd ' + origin_path)
    os.system(add)
    os.system(commit)
    os.system(push)

while 1:
    update_all()
    push_origin()
    time.sleep(3600)