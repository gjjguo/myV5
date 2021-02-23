#coding:utf-8
'''
审核接口,依赖于登录接口和添加项目接口，从登录接口中获取token，从添加项目接口中获取loan_id
项目审核只能是管理员进行审核，依赖于管理员登录接口
'''
from jsonpath import jsonpath
import requests
import json
import pytest
from middleware.handler import Handler
# 从Excel读取数据
data = Handler.excel.read_excel('audit')
@pytest.mark.parametrize('data', data)
def test_audit(data,admin_login,add_loan):
    print(add_loan)
    print(admin_login)
    #请求参数
    headers=data['headers']
    request_data=data['data']
    url=data['url']
    method=data['method']
    expected=data['expected']
    #判断：
    if "#token#" in headers:
        headers=headers.replace("#token#",admin_login['token'])
    if "#loan_id#" in request_data:
        request_data=request_data.replace("#loan_id#",str(add_loan))
    headers=json.loads(headers)
    request=json.loads(request_data)
    #发送数据
    response=requests.request(method=method,
                             url=Handler.config_yaml['host']+url,
                             headers=headers,
                             json=request)
    result=response.json()
    print(result)
    expected=json.loads(expected)
  
    for key, value in expected.items():
        try:
            print(key)
            print(value)
            assert jsonpath(result, key)[0]==value
            Handler.logger.error("测试用例执行成功,请求头为{},请求体为{}".format(headers,request))
        except AssertionError as err:
            Handler.logger.error("测试用例执行失败{},请求头为{},请求体为{}".format(err,headers,request))
            raise err
        finally:
            Handler.excel.write_excel('audit',
                                     colnum=9,
                                     row=int(data['case_id'])+1,
                                     data=str(result))

    