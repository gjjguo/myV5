# coding:utf-8
'''注册接口'''
import json
from middleware.handler import Handler
import requests
import pytest

test_data = Handler.excel.read_excel('register')


@pytest.mark.parametrize('test_data', test_data)
def test_register(test_data):
    '''注册接口测试用例'''
    # 准备测试数据
    url = test_data['url']
    data = test_data['data']
    method = test_data['method']
    headers = test_data['headers']
    expected = test_data['expected']
    '''
    1.读取method数据
    2.存在#new_phone#
    3.生成新的手机号码
    4.替换
    '''
    if '#new_phone#' in data:
        phone = Handler.generate_new_phone()
        print(phone)
        # 替换
        data = data.replace('#new_phone#', phone)
    # 访问接口
    res = requests.request(method=method,
                           headers=json.loads(headers),
                           url=Handler.config_yaml['host'] + url,
                           json=json.loads(data))
    # 获取响应体
    res_body = res.json()
    # 将断言加上异常处理，方便用例执行失败后添加失败日志到日志文件中
    try:
        assert res_body['code'] == expected
        Handler.logger.info('用例执行成功{}'.format(data))
    except AssertionError as err:
        Handler.logger.error('用例执行失败{}'.format(err, data))
        # 将捕获的异常抛出
        raise err
    finally:
        Handler.excel.write_excel(sheet_name='register',
                                  colnum=8,
                                  row=int(test_data['case_id']) + 1,
                                  data=str(res_body))
