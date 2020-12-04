import configparser
import os

conf = configparser.ConfigParser()


def readConf():
    # logger = logging.getLogger("readConf")
    # 获取当前文件的路径
    root_path = os.path.dirname(os.path.abspath(__file__))

    # logger.info(root_path)
    if root_path.find('\\') != -1:

        conf.read(root_path + '\config\config.ini')
        # logger.info("readConfig:{}".format(root_path + '\config\config.ini'))
    else:
        conf.read(root_path + '/config/config.ini')
    minerID = conf.get("miner", "minerID")
    ##logger.info("minerID:{}".format(minerID))
    # return minerID
    print(minerID)


readConf()
