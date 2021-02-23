# coding:utf-8
'''帮助模块'''
import random
from faker import Faker
from common.db_handler import DBHandler


def generate_new_phone():
    '''自动生成手机号'''
    fk = Faker(locale='zh_CN')
    while True:
        phone = fk.phone_number()
        # 查询手机号是否在数据库中存在,如果不存在，返回新生成的手机号，如果存在，重新生成手机号
        db_phone = DBHandler(host=config_yaml['db']['host'],
                             port=config_yaml['db']['port'],
                             user=config_yaml['db']['user'],
                             password=config_yaml['db']['password'],
                             database=config_yaml['db']['database'])
        db_in_phone = db_phone.query("select mobile_phone from member where mobile_phone='{}'".format(phone))
        # 没有查询出来，就将手机号返回
        if not db_in_phone:
            return phone


'''
第二种方式
def get_moblie():
    #通过随机数生成手机号#
    while True:
        phone = '1' + random.choice(['3', '4', '5', '6', '7', '8'])
        for i in range(9):
            number = random.randint(1, 9)
            phone += str(number)
        return phone
'''

if __name__ == '__main__':
    # S=generate_new_phone()
    # print(S)
    phone = generate_new_phone()
    print(phone)
