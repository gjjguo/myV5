# coding:utf-8
'''
更新昵称接口，前置条件：依赖于登录接口
'''
import json

import pytest
import requests
from middleware.handler import Handler

data = Handler.excel.read_excel("updatanicheng")


@pytest.mark.parametrize('data', data)
def test_upfdate_name(data, investor_login):
    # 请求的数据
    url=data['url']
    headers = data['headers']
    if '#token#' in headers:
        headers = headers.replace('#token#', investor_login['token'])
    json_data = data['json']
    if '#member_id#' in json_data:
        json_data = json_data.replace('#member_id#', str(investor_login['id']))
    reponse = requests.request(method=data['method'],
                               url=Handler.config_yaml['host']+url,
                               headers=json.loads(headers),
                               json=json.loads(json_data)
                               )
    result = reponse.json()
    try:
        assert result['code'] == data['expected']
        Handler.logger.info("用例执行成功,请求头为{}，请求体为{}，响应结果为{}".format(headers, json_data, result))
    except  AssertionError as err:
        Handler.logger.error("用例执行失败{},请求头为{}，请求体为{}，响应结果为{}".format(err, headers, json_data, result))
        raise err
    finally:
        Handler.excel.write_excel(sheet_name='updatanicheng',
                                  colnum=8,
                                  row=int(data['case_id']) + 1,
                                  data=str(result))
