# coding:utf-8
'''
项目列表接口
前置条件：
1.借款人登录新增项目，并且查看新增的项目信息
2.管理员登录查看待审核的项目信息
'''
import pytest
import requests

from middleware.handler import Handler
import json
from jsonpath import jsonpath
data=Handler.excel.read_excel("loanlist")
@pytest.mark.parametrize('data',data)
def test_loan_list(data):
    #获取Excel中的数据，并将数据转成json格式的字符串
    data=json.dumps(data)
    #将Excel中的#str#调用方法替换
    data=Handler.replace_data(string=data)
    #再将data格式的字符串转为字典格式
    data=json.loads(data)
    headers=json.loads(data['headers'])
    expected=json.loads(data['expected'])
    json_data=json.loads(data['json'])
    reponse=requests.request(method=data['method'],
                             url=Handler.config_yaml['host']+data['url'],
                             headers=headers,
                             json=json_data)
    result=reponse.json()
    try:
        for key ,value in expected.items():
            #key=code,value=0
            assert jsonpath(result,key)[0]==value
            if data['extractor']:
                extractors=json.loads(data['extractor'])
                for handle_pro,jsonpath_value in extractors.items():
                    values=jsonpath(result,jsonpath_value)[0]
                    setattr(Handler,handle_pro,values)
            Handler.logger.info("用例执行成功,请求头为{}，请求体为{},响应为{}".format(headers,json_data,result))
    except AssertionError as err:
        Handler.logger.error("用例执行失败{}，请求头为{}，请求体为{}，响应为{}".format(err,headers,json_data,result))
        raise err
    finally:
        Handler.excel.write_excel(sheet_name='loanlist',
                                  colnum=9,
                                  row=int(data['case_id'])+1,
                                  data=str(result))


