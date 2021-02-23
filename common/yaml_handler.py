# coding:utf-8
'''读取yaml配置文件数据'''

import yaml



def read_yaml(file_path):
    '''读取yaml文件'''
    with open(file_path, encoding='utf-8') as wstream:
        data = yaml.load(wstream, Loader=yaml.SafeLoader)
    return data




