# -*-coding:utf-8-*-
'''
运行日志的封装，函数封装 def get_logger()
'''

import logging


# 定义logger收集器函数
def get_logger(name=None, logger_level=logging.INFO, cmd_level=logging.DEBUG, file_level=logging.INFO,
               filename=None):
    """定义收集器和处理器函数"""
    # 定义收集器
    logger = logging.getLogger(name)
    # 定义收集器的级别
    logger.setLevel(logger_level)
    # 添加处理器的格式
    format = logging.Formatter('%(name)s-[%(asctime)s]-[%(levelname)s]-%(filename)s-%(message)s-%(lineno)d ')
    # 定义控制台处理器
    consol_handle = logging.StreamHandler()
    consol_handle.setLevel(cmd_level)
    consol_handle.setFormatter(format)
    logger.addHandler(consol_handle)
    # 判断如果filename有值的话，就执行文件处理器的操作，如果没有就不执行
    if filename:
        file_handle = logging.FileHandler(filename, encoding='utf-8')
        file_handle.setLevel(file_level)
        file_handle.setFormatter(format)
        logger.addHandler(file_handle)
    return logger


# 获取logs的路径
#filepath = path.logs_path
# 以时间为日志文件名
#time_file = datetime.now().strftime('%Y-%m-%d')
#filename = os.path.join(filepath, time_file + '.log')
#logger = get_logger(filename=filename)
