#coding:utf-8
'''
测试夹具函数，实现测试用例的前置和后置
'''
# 测试夹具
import pytest
from middleware.handler import Handler
from jsonpath import jsonpath
import requests


def login(user, pwd):
    """最终返回id ，token，leave_amount"""
    login_data = {"mobile_phone": user, "pwd": pwd}
    res = requests.request(url=Handler.config_yaml['host'] + '/member/login',
                           method='post',
                           headers={"X-Lemonban-Media-Type": "lemonban.v2"},
                           json=login_data)
    response_result = res.json()
    member_id = jsonpath(response_result, '$..id')[0]
    token = jsonpath(response_result, '$..token')[0]
    token_type = jsonpath(response_result, '$..token_type')[0]
    token = ' '.join([token_type, token])
    leave_amount = jsonpath(response_result, '$..leave_amount')[0]

    return {"id": member_id, "token": token, "leave_amount": leave_amount}


# 借款人人登录
@pytest.fixture()
def investor_login():
    """调用login函数，将借款人信息传递给login函数"""
    investor_data = {"mobile_phone": Handler.security_yaml['investor_user']['phone'],
                     "pwd": Handler.security_yaml['investor_user']['pwd']}

    return login(investor_data['mobile_phone'], investor_data['pwd'])



# 借款人人登录
@pytest.fixture()
def loan_login():
    """最终返回id ，token，leave_amount"""
    investor_data = {"mobile_phone": Handler.security_yaml['loan_user']['phone'],
                     "pwd": Handler.security_yaml['loan_user']['pwd']}
    return login(investor_data['mobile_phone'], investor_data['pwd'])


# 管理员登录
@pytest.fixture()
def admin_login():
    """最终返回id ，token，leave_amount"""
    investor_data = {"mobile_phone": Handler.security_yaml['admin_user']['phone'],
                     "pwd": Handler.security_yaml['admin_user']['pwd']}
    return login(investor_data['mobile_phone'], investor_data['pwd'])


# 添加项目
@pytest.fixture()
def add_loan(loan_login):
    """添加项目"""
    loan_data = {"member_id": int(loan_login['id']),
                 "title": "工程款",
                 "amount": 6300,
                 "loan_rate": 18,
                 "loan_term": 6,
                 "loan_date_type": 1,
                 "bidding_days": 5}
    print(loan_login['token'])
    headers = {'X-Lemonban-Media-Type': 'lemonban.v2', 'Authorization': loan_login['token']}
    response = requests.request(method='POST',
                                headers=headers,
                                json=loan_data,
                                url=Handler.config_yaml['host'] + '/loan/add')
    result = response.json()
    loan_id = jsonpath(result, '$..id')[0]
    return int(loan_id)

@pytest.fixture()
def db():
    """管理数据库的连接的夹具"""
    db_coon = Handler.db_class
    yield db_coon
    # db_coon.close()


# if __name__ == '__main__':
#    s=add_loan(loan_login)
#    print(s)



