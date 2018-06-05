# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 下午3:54
# @Author  : 大兵
import os
import sys

BASEDIR = "/Users/dabing/.virtualenvs/test/lib/python3.6/site-packages"
sys.path.append(BASEDIR)

import paramiko
from collect.test_log import Loger
class Collect_Data:

    def __init__(self,hostname,password,username="ops",port=22):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password =password
        # self.ssh()

    def ssh(self):
        # 创建连接
        self.jssh = paramiko.SSHClient()
        self.jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            key=paramiko.RSAKey.from_private_key_file('collect/ser')
            self.jssh.connect(hostname=self.hostname, port=self.port, username="ops", pkey=key,timeout=6)
        except Exception as e:
            print("证书=======",e)
            # Loger('info',self.hostname+'证书连接失败，尝试密码')
            try:
                self.jssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password,timeout=6)  # pkey=private_key
            except Exception as e:
                print("password=======",e)
                # Loger('info',self.hostname+'密码连接失败')
                return 'failed'

    def exec_cmd(self,CMD):
        stdin, stdout, stderr = self.jssh.exec_command(CMD)
        stdout = stdout.read()
        stderr = stderr.read()

        if stdout:
            output = stdout
        else:
            output = b"error "+stderr

        #return output
        return stdout+stderr

    def close_conn(self):
        self.jssh.close()


# conn = Collect_Data(hostname="192.168.15.192", port=22,username='ops',password="aaa")
# print(conn.ssh())
# print(conn.exec_cmd("sudo hostname -i").decode('utf-8').strip().split('\n')[0])
