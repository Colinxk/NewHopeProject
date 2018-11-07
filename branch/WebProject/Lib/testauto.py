# -*- coding: UTF-8 -*-
import os, time, subprocess, sys, csv



def read_csv_file(input_value):
    '''
    读取数据文件
    input_value:    所选的环境
    '''
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    print  BASE_DIR
    file_path = os.path.join(BASE_DIR, 'Data', 'Data.csv')
    for var in csv.DictReader(open(file_path)):
        if var['No']==input_value:
            break
    return var

print 111
