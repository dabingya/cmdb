# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 下午2:10
# @Author  : 大兵


import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)

# import paramiko
#
# class Collect_Data:
#
#     def __init__(self,hostname,password,username="root",port=22):
#         self.hostname = hostname
#         self.port = port
#         self.username = username
#         self.password =password
#         self.ssh()
#
#     def ssh(self):
#         # 创建连接
#         self.jssh = paramiko.SSHClient()
#         self.jssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         self.jssh.connect(hostname=self.hostname, port=self.port, username=self.username, password=self.password)  # pkey=private_key
#
#
#     def exec_cmd(self,CMD):
#         stdin, stdout, stderr = self.jssh.exec_command(CMD)
#         stdout = stdout.read()
#         stderr = stderr.read()
#
#         if stdout:
#             output = stdout
#         else:
#             output = b"error "+stderr
#
#         return output

# cc = Collect_Data('192.168.9.91','dabingya')
#
# ret = cc.exec_cmd("fdifsk -l |grep 'Linux'| awk -F'[/ *]+' '{print $3,$6}'")
#
# content = ret.strip()
# for item in content.decode('utf-8').split('\n\n'):
#     print(item)


from collect.test_log import Loger




Loger('info',"info")
Loger('error',"发生了一些错误！ 1111")
Loger('info',"info2222")
