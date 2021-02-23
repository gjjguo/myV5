# -*- coding: utf-8 -*-
import pytest
from middleware.handler import Handler
import json
import requests

'''
1.获取测试用例的路径，需要导入config下的path模块
2.从excel中读取测试用例，需要导入Excel操作模块
'''


login_data = Handler.excel.read_excel('login')


@pytest.mark.parametrize('login_data', login_data)
def test_login(login_data):
    '''登录接口测试用例'''
    # 获取登录的数据
    url = login_data['url']
    request_data = login_data['data']
    method = login_data['method']
    headers = login_data['headers']
    expected = login_data['expected']

    if "*phone*" in request_data:
        new_phone = Handler.generate_new_phone()
        request_data = request_data.replace('*phone*', new_phone)
    if "#phone#" in request_data:
        phone = Handler.security_yaml['investor_user']['phone']
        request_data = request_data.replace('#phone#', phone)
    if "#pwd#" in request_data:
        new_pwd = Handler.security_yaml['investor_user']['pwd']
        request_data = request_data.replace('#pwd#', new_pwd)

    # 请求登录接口
    reponse = requests.request(url=Handler.config_yaml['host'] + url,
                               headers=json.loads(headers),
                               method=method,
                               json=json.loads(request_data))
    reps_data = reponse.json()
    try:
        assert expected == reps_data['code']
        Handler.logger.info('用例执行成功{}'.format(request_data))
    except AssertionError as err:
        Handler.logger.error('用例执行失败{},{}'.format(err, request_data))
        raise err
    finally:
        # 将返回的json写入到Excel中
        Handler.excel.write_excel(sheet_name='login',
                                                 row=int(login_data['case_id']) + 1,
                                                 colnum=8,
                                                 data=str(reps_data))
