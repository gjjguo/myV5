# coding:utf-8
'''负责主程序的入口，收集用例，运行用例，生成报告'''
from config import path
from datetime import datetime
import os
import pytest
from middleware.handler import Handler
#引入测试报告路径变量
report_path=path.report_path
file_format=datetime.now().strftime('%Y-%m-%d')
file_name=os.path.join(report_path,'report-'+file_format+'.html')

# sender =Handler.config_yaml['email']['sender']
# revicer = Handler.config_yaml['email']['revicer'][0]
# content = Handler.config_yaml['email']['content']
# subject = Handler.config_yaml['email']['subject']
# file_name_abs=os.path.abspath(file_name)
# filename=os.path.basename(file_name_abs)
# Handler.email.send_email(filepath=file_name_abs,
#                  filename=filename,
#                  sender=sender,
#                  revicer=revicer,
#                  content=content,
#                  subject=subject)

pytest.main(['--html={}'.format(file_name),'-vs'],)
