# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 按两次 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
# coding=utf-8

import logging
import os
from datetime import date, timedelta
import configparser

import pymysql as pymysql

logging.basicConfig(level=logging.INFO, format='%(asctime)-10s    %(levelname)-10s    %(name)-20s        %(message)-s')

conf = configparser.ConfigParser()

#读取minerID
def readConf_miner():
    _logger = logging.getLogger("readConf_miner")
    # 获取当前文件的路径
    root_path = os.path.dirname(os.path.abspath(__file__))

    #_logger.info(root_path)

    if root_path.find('\\') != -1:
        path = root_path + '\config\config.ini'
    else:
        path = root_path + '/config/config.ini'
    conf.read(path, encoding='utf-8')
    minerID = conf.get("miner", "minerID")
    _logger.info("minerID:{}".format(minerID))
    return minerID

#读取数据库配置
def readConf_db():
    _logger = logging.getLogger("readConf_db")
    # 获取当前文件的路径
    root_path = os.path.dirname(os.path.abspath(__file__))

    if root_path.find('\\') != -1:
        path = root_path + '\config\config.ini'

    else:
        path = root_path + '/config/config.ini'
    _logger.info(path)
    conf.read(path, encoding='utf-8')
    db_host = conf.get("database", "db_host")
    db_name = conf.get("database", "db_name")
    db_port = int(conf.get("database", "db_port"))
    db_user = conf.get("database", "db_user")
    db_password = conf.get("database", "db_password")
    db = {'db_host': db_host, 'db_name': db_name, 'db_port': db_port, 'db_user': db_user, 'db_password': db_password}
    return db

#截取日志
def miner_log_cut():
    _logger = logging.getLogger("miner_log_cut")
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path.find('\\') != -1:
        path = root_path + '\config\config.ini'

    else:
        path = root_path + '/config/config.ini'
    conf.read(path)
    miner_Log_path = conf.get("miner_log", "path")
    # 获取当前日期的前一天日期，并格式化输出
    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    _logger.info(yesterday)
    # 获取前一天的日志到临时文件中
    val = os.system(
        "sed -n /{}/,/{}/p {} >./miner-log.tmp ".format("2020-11-08T00:00:00", "2020-11-08T23:59:59", miner_Log_path))
    # print("日志提取: {}".format(val))
    _logger.info("日志提取：{}".format(val))
    if root_path.find('\\') != -1:
        log_ptah = root_path + '\miner-log.tmp'
    else:
        Log_path = root_path + '/miner-log.tmp'
    return log_ptah

#获取日志path
def miner_log():
    _logger = logging.getLogger("miner_log")
    root_path = os.path.dirname(os.path.abspath(__file__))
    if root_path.find('\\') != -1:
        path = root_path + '\config\config.ini'

    else:
        path = root_path + '/config/config.ini'
    conf.read(path)
    miner_Log_path = conf.get("miner_log", "path")
    _logger.info(miner_Log_path)
    return miner_Log_path


def read_log():
    _logger = logging.getLogger("read_log")
    # path = miner_log_cut()
    path = miner_log()
    mined_list = []
    # 打开日志文件，读取信息
    with open("{}".format(path), 'r', encoding='utf-8') as log:
        lines = log.readlines()
        _logger.info("open {}".format(path))
        for line in lines:
            line1 = line.strip()
            # 获取出块信息
            if line1.find("mined") != -1:
                new_mined = line1.split('"')[3].strip()
                # logger.info("new mined: {}".format(new_mined))
                new_mined_time = line1.split('+')[0].replace("T", " ").split('.')[0].strip()
                # logger.info("new mined time: {}".format(new_mined_time))
                new_mined_finished_time = line1.split('took')[1].split(':')[1].split('}')[0].strip()
                # logger.info("new mined finished time: {}s".format(new_mined_finished_time))
                _mined = {'mined': new_mined, 'mined_time': new_mined_time,
                          'mined_finished_time': new_mined_finished_time}
                mined_list.append(_mined)
    _logger.info("return mined list")
    return mined_list

# 导入数据库
def sql():
    _logger = logging.getLogger("sql")
    db_info = readConf_db()
    # 打开数据库连接
    conn = pymysql.connect(db_info['db_host'], db_info['db_user'], db_info['db_password'], db=db_info['db_name'],
                           port=db_info['db_port'])
    # 获取游标
    cursor = conn.cursor()
    _logger.info(cursor)

    miner_id = readConf_miner()
    #获取 出块列表
    minedes = read_log()
    _logger.info("开始导入数据库")
    for mined in minedes:
        sql = "insert ignore into mined(miner_id, mined_cid, mined_time, mined_finished_time) values ('{}', '{}', '{}', {});".format(miner_id, mined['mined'], mined['mined_time'], mined['mined_finished_time'])
        cursor.execute(sql)
        conn.commit()
        _logger.info(mined['mined'] + "  插入成功")
    _logger.info("插入{}条数据，导入结束".format(len(minedes)))
    conn.close()

def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'{name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    _logger = logging.getLogger("read_log")
    print_hi('Hello,beck!')
    sql()


# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
