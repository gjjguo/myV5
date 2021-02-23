# coding:utf-8
'''通过上课学的知识，把mysql数据库封装成类 DBHandler'''
import pymysql
from pymysql.cursors import DictCursor
class DBHandler:
    def __init__(self, host='',
                 port=3306,
                 user='',
                 password='',
                 database=''):
        # 数据库连接
        self.conn = pymysql.connect(host=host,
                                    port=port,
                                    user=user,
                                    password=password,
                                    database=database,
                                    charset='utf8',
                                    cursorclass=DictCursor
                                    )
        # # 获取数据库游标

    def query(self, sql, one=True):
        '''查询数据库'''

        self.cursor = self.conn.cursor()
        self.conn.commit()
        self.cursor.execute(sql)

        if one:
           data= self.cursor.fetchone()
           self.cursor.close()
           return data
        self.cursor.close()
        data= self.cursor.fetchall()
        return data


    def insert(self, sql):
        '''在数据库中插入数据'''
        # 获取数据库游标
        self.cursor = self.conn.cursor()

        self.cursor.execute(sql)
        # 提交
        self.conn.commit()

    def delete(self, sql):
        '''删除数据库中的数据'''
        # 获取数据库游标
        self.cursor = self.conn.cursor()

        self.cursor.execute(sql)
        # 提交
        self.conn.commit()

    def update(self, sql):
        '''更新数据库中的数据'''
        # 获取数据库游标
        self.cursor = self.conn.cursor()
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        '''关闭数据库'''
        # 关闭游标
        self.cursor.close()
        # 关闭数据库
        self.conn.close()


if __name__ == '__main__':
    database = DBHandler(host='8.129.91.152',
                         port=3306,
                         user='future',
                         password='123456',
                         database='futureloan')
    # print(database)
    # 查询数据
    data = database.query("SELECT leave_amount FROM member WHERE id='1348'")
    print(data)
    database.close()
