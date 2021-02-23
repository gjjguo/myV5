# coding:utf-8
'''Excel操作'''


import openpyxl


class ExcelHandler:
    def __init__(self, test_file):
        self.test_file = test_file

    def read_excel(self, sheet_name):
        '''读取Excel数据方法'''
        # 打开Excel
        work_book = openpyxl.open(self.test_file)
        # 获取sheet页的数据
        work_sheet = work_book[sheet_name]
        # 获取所有的数据
        sheet_data = list(work_sheet.values)
        # 将元组转为字典
        header = sheet_data[0]
        test_data = []
        for row in sheet_data[1:]:
            # 使用zip将两个列表合并为字典
            row_dict = dict(zip(header, row))
            # 将测试数据添加到列表里面
            test_data.append(row_dict)
        return test_data

    def write_excel(self, sheet_name, row, colnum, data):
        '''将测试的响应结果写入到Excel中'''
        work_book = openpyxl.open(self.test_file)
        work_sheet = work_book[sheet_name]
        # 写入文件到Excel中
        write_data = work_sheet.cell(row, colnum).value = data
        work_book.save(self.test_file)
        work_book.close()


if __name__ == '__main__':
    xls = ExcelHandler('case.xlsx')
    test = xls.read_excel('addproject')
    print(test)
    w = xls.write_excel(sheet_name='login', row=2, colnum=8, data='pass')
