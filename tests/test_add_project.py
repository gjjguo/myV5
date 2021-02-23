# coding:utf-8
'''添加项目接口'''
import jsonpath
import requests
import json
import pytest
from middleware.handler import Handler

# 从Excel读取数据
data = Handler.excel.read_excel('addproject')
@pytest.mark.parametrize('data', data)
def test_add_project(data, investor_login):
    method = data['method']
    headers = data['headers']
    url = data['url']
    request_data = data['data']
    expected = data['expected']
    if "#member_id#" in request_data:
        request_data = request_data.replace('#member_id#', str(investor_login['id']))
    if "#token#" in headers:
        headers = headers.replace('#token#', investor_login['token'])
    if "#wong_token#" in headers:
        headers = headers.replace('#wong_token#', investor_login['token'] + 'adf')
    response = requests.request(method=method,
                                headers=json.loads(headers),
                                url=Handler.config_yaml['host'] + url,
                                json=json.loads(request_data))
    result = response.json()
    try:
        assert expected == result['code']
        Handler.logger.info("执行成功,请求体为{}".format(request_data))
    except AssertionError as err:
        Handler.logger.error("用例执行失败{}，headers为{}，请求体为{}".format(err,headers,request_data))
        raise err
    finally:
        Handler.excel.write_excel(sheet_name='addproject',
                                                 colnum=9,
                                                 row=int(data['case_id'])+1,
                                                 data=str(result))
