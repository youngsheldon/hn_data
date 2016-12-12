#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: anchen
# @Date:   2016-12-09 11:14:43
# @Last Modified by:   anchen
# @Last Modified time: 2016-12-12 11:59:52
import os
import time

bug_data_path = '/opt/smmc/apk_parse/entire_apk_report_run/data/'
origin_path = '/opt/smmc/apk_parse/hn_data/'
apk_path = '/opt/smmc/data_backup/apk/'

class PushBug(object):
    def get_datetime(self):
        return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    def update(self,file_name):
        out = 'cat ' + bug_data_path + file_name + ' > ' + origin_path + file_name
        os.system(out)

    def update_all(self):
        self.update('log.txt')
        self.update('md5.txt')
        self.update('problem_apk.txt')
        self.bug_out_to_file()
        self.get_pro_apk_relate_isue()

    def push_origin(self):
        add = 'git add --all'
        commit = 'git commit -m ' + '\"' + self.get_datetime() + '\"' 
        push = 'git push origin master'
        os.system('cd ' + origin_path)
        os.system(add)
        os.system(commit)
        os.system(push)

    def get_problem_md5(self):
        pro_md5_list = []
        with open('problem_apk.txt','r') as f:
            for line in f:
                v = line.strip()
                pro_md5_list.append(v)
        return pro_md5_list

    def get_bug_list(self):
        bug_list = []
        with open('log.txt','r') as f:
            tmp = ''
            index = 0 
            for line in f:
                if 'ERROR' in line:
                    index += 1 
                if index > 0:
                    if 'INFO' not in line:
                        tmp += line
                    else:
                        bug_list.append(tmp)
                        tmp = ''
                        index = 0 
        return bug_list

    def sort_bug_list(self):
        bug_dict = {}
        v_list = []
        l = self.get_bug_list()
        for v in l:
            error_type = v.split('\n')[-2]
            bug_dict[error_type] = v
        for k,v in bug_dict.items():
            for value in l:
                error_type = value.split('\n')[-2]
                if error_type == k:
                    v_list.append(value)
            bug_dict[k] = v_list
            v_list = []    
        return bug_dict

    def bug_out_to_file(self):
        ret_dict = self.sort_bug_list()
        with open('bug_out.txt','w+') as f:
            for k,vs in ret_dict.items():
                f.write('-------------------' + k + '-----------------------' + '\n')
                for value in vs:
                    f.write(value)
                f.write('\n')

    def get_pro_apk_relate_isue(self):
        pro_md5_list = self.get_problem_md5()
        for md5 in pro_md5_list:
            xml_path = apk_path + md5 + '.xml'
            log_path = apk_path + md5 + '.log'
            xml_out = 'cat ' + xml_path + ' > ' + 'apkData/' + md5 + '.xml'
            log_out = 'cat ' + log_path + ' > ' + 'apkData/' + md5 + '.log'
            os.system(xml_out)
            os.system(log_out)

    def run(self):
        self.update_all()
        self.push_origin()

while 1:
    obj = PushBug()
    obj.run()
    time.sleep(3600*24)
