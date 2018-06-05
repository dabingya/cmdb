# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 下午6:00
# @Author  : 大兵

import logging

def Loger(status,msg):

    logger = logging.getLogger("收集资产")
    logger.setLevel(level=logging.INFO)

    handler = logging.FileHandler("../new_cmdb/log/log.txt")
    handler.setLevel(level=logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    logger.addHandler(handler)

    if status == "info":
        logger.info(msg)
    elif status == "error":
        logger.error(msg)
    logger.removeHandler(handler)
