# coding:utf-8
'''获取用户个人信息接口
依赖接口：登录接口，获取登录接口的token和member_id的值
'''
import json

import pytest
import requests

from middleware.handler import Handler
data=Handler.excel.read_excel("userinfo")
@pytest.mark.parametrize('data',data)
def test_get_userinfo(data,investor_login):
    #获取请求数据
    headers = data['headers']
    if '#token#' in headers:
        headers = headers.replace('#token#', investor_login['token'])
    if "#wrong_token#" in headers:
        headers = headers.replace('#wrong_token#', investor_login['token']+'ass')
    url=data['url']
    if '{member_id}' in url:
        url=url.replace('{member_id}',str(investor_login['id']))

    method=data['method']
    reponse=requests.request(method=method,
                             url=Handler.config_yaml['host']+url,
                             headers=json.loads(headers))
    result=reponse.json()
    try:
        assert result['code']==data['expected']
        Handler.logger.info("用例执行失败成功,请求头为{}，请求体为{},响应结果为{}".format(headers, url, result))
    except AssertionError as err:
        Handler.logger.error("用例执行失败{},请求头为{}，请求体为{},响应结果为{}".format(err,headers,url,result))
        raise err
    finally:
        Handler.excel.write_excel(sheet_name='userinfo',
                                  colnum=7,
                                  row=int(data['case_id'])+1,
                                  data=str(result))
