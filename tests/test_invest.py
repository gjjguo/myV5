#coding:utf-8
'''
投资项目测试用例：前置条件:
1.投资人登录，进行投资
2.借款人登录，添加项目
3.管理员登录，审核项目
'''
import json

import requests
from jsonpath import jsonpath

from middleware.handler import Handler
import pytest
excel_data=Handler.excel.read_excel('investor')
@pytest.mark.parametrize('data',excel_data)
def test_invest(data):
    #获取Excel中所有的数据
    #将所有的数据转为json格式的字符串，获取#str#数据完成替换
    data=json.dumps(data)
    data=Handler.replace_data(string=data)
    #将替换完成的数据转为字典
    data=json.loads(data)
    #请求数据
    url=data['url']
    method=data['method']
    headers=data['headers']
    request_data=json.loads(data['json'])
    #添加请求
    reponse=requests.request(url=Handler.config_yaml['host']+url,
                             method=method,
                             headers=json.loads(headers),
                             json=request_data)
    result=reponse.json()
    #多值断言
    try:
        for key,value in result.items():
            #key=code,value=0
            assert jsonpath(result,key)[0]==value
            #提取响应结果，设置handle对应的属性
            if data['extractor']:
                extractors=json.loads(data['extractor'])
                for handle_pro,jsonpath_exp in extractors.items():
                    values=jsonpath(result,jsonpath_exp)[0]
                    print('--------values-----',values)
                    setattr(Handler,handle_pro,values)
            Handler.logger.info("用例执行成功，请求头{},请求体为{}".format(headers, request_data))


    except AssertionError as err:
                Handler.logger.error("用例执行失败{}，请求头{},请求体为{}".format(err,headers,request_data))
                raise err
    finally:
        Handler.excel.write_excel(sheet_name='investor',
                                  colnum=9,
                                  row=int(data['case_id'])+1,
                                  data=str(result))

