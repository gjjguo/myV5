# coding:utf-8
'''提取现金接口'''

import json
import pytest
import requests
from middleware.handler import Handler
from decimal import Decimal

# 从Excel读取数据
data = Handler.excel.read_excel('withdrawal')


@pytest.mark.parametrize('data', data)
def test_extract_money(data, investor_login,db):
    '''提现金额测试用例'''
    # 获取登录的数据
    url = data['url']
    request_data = data['data']
    method = data['method']
    headers = data['headers']
    expected = data['expected']
    if '#member_id#' in request_data:
        request_data = request_data.replace('#member_id#', str(investor_login['id']))
    if '#wrong_member_id#' in request_data:
        request_data = request_data.replace('#wrong_member_id#', str(investor_login['id'] + 1))
    # 数据库的访问，充值之前的余额
    sql = "SELECT leave_amount FROM member WHERE id={}".format(investor_login['id'])
    result = db.query(sql)
    befor_money = result['leave_amount']
    # 通过代码组装token的值
    headers = json.loads(headers)
    headers['Authorization'] = investor_login['token']
    request_args = json.loads(request_data)
    response = requests.request(url=Handler.config_yaml['host'] + url,
                                method=method,
                                headers=headers,
                                json=request_args)
    response_result = response.json()
    try:
        # 断言
        assert response_result['code'] == expected
        Handler.logger.info("用例执行成功headers:{},请求{}".format(headers, request_data))
    except AssertionError as err:
        Handler.logger.error("用例执行失败错误原因{},headers为：{},请求为：{}".format(err, headers, request_data))
    finally:
        Handler.excel.write_excel('withdrawal',
                                  row=int(data['case_id']) + 1,
                                  colnum=9,
                                  data=str(response_result))
    if response_result['code'] == 0:
        sql = "SELECT leave_amount FROM member WHERE id={}".format(investor_login['id'])
        result = db.query(sql)
        after_money = result['leave_amount']
        money = Decimal(str(request_args['amount']))
        try:
            assert befor_money == after_money - money
            Handler.logger.info("用例执行成功,提取之前的余额{}，提取的钱为{}，提取后剩余的余额{}".format(befor_money, money, after_money))

        except AssertionError as err:
            Handler.logger.error(
                "用例执行失败错误原因{},提取之前的余额{}，提取的钱为{}，提取后剩余的余额{}".format(err, befor_money, money, after_money))
            raise err
        finally:
            Handler.excel.write_excel('withdrawal',
                                      row=int(data['case_id']) + 1,
                                      colnum=8,
                                      data=str('提取之前的余额{}，提取的钱为{}，提取后剩余的余额{}'.format(befor_money, money,
                                                                                     after_money)))
