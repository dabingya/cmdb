# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 下午3:55
# @Author  : 大兵

import os
import sys
BASEDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASEDIR)
from collect.collect_data import Collect_Data
from collect.test_log import Loger

class Data:
    def __init__(self,ip,username,port,password):
        self.ip = ip
        self.username = username
        self.port = port
        self.password = password

    def make_data(self):
        hostname_cmd = "sudo hostname"
        sys_version_cmd = "sudo cat /etc/redhat-release"
        kernel_cmd = "sudo uname -r"
        cputype_cmd= "sudo cat /proc/cpuinfo |grep 'model name'|awk -F':' 'NR==1{print $2}'"
        cpunum_cmd = "sudo cat /proc/cpuinfo |grep '^processor'| wc -l"
        mem_cmd = "sudo dmidecode  -q -t 17 2 |awk '$1~/Size/{print $2$3}'"
        swap_cmd = "sudo free -m|grep 'Swap'|awk '{print $2}'"
        disk_cmd ="sudo fdisk  -l |egrep -w 'Disk|磁盘'|grep -v 'docker'|egrep -v 'identifier|type' |awk -F'[ :/：,]+' '{print $3,$4$5}'"
        ip_cmd = "sudo hostname -i"

        dict = {
            "hostname":None,
            "sys_version": None,
            "kernel":None,
            "cputype": None,
            "cpunum": None,
            "mem": None,
            "swap": None,
            "disk": {},
            "ip":None,
        }

        try:
            conn = Collect_Data(hostname=self.ip, username=self.username,port=self.port,password=self.password)
            get_conn = conn.ssh()
            if get_conn == "failed":
                # print("aaaaa")
                return "failed"
            # 主机名
            dict['hostname'] = conn.exec_cmd(hostname_cmd).decode('utf-8').strip().split('\n')[0]
            # 系统版本
            dict["sys_version"] = conn.exec_cmd(sys_version_cmd).decode('utf-8').strip().split('\n')[0]
            # 内核版本
            dict["kernel"] = conn.exec_cmd(kernel_cmd).decode('utf-8').strip().split('\n')[0]
            # CPU型号
            dict["cputype"] = conn.exec_cmd(cputype_cmd).decode('utf-8').strip().split('\n')[0]
            # CPU个数
            dict["cpunum"] = conn.exec_cmd(cpunum_cmd).decode('utf-8').strip().split('\n')[0]
            # 内存
            dict["mem"] = conn.exec_cmd(mem_cmd).decode('utf-8').strip().split('\n')[0]
            # SWAP
            dict["swap"] = conn.exec_cmd(swap_cmd).decode('utf-8').strip().split('\n')[0]+"MB"
            # 硬盘
            for item in conn.exec_cmd(disk_cmd).decode('utf-8').strip().split('\n'):
                dict["disk"][item[:3]] = item.split(' ')[1]
            # 内网ip
            dict["ip"] = conn.exec_cmd(ip_cmd).decode('utf-8').strip().split('\n')[0]

            Loger('info', self.ip+" 资产收集成功")
            conn.close_conn()
            return  dict
        except Exception as e:
            Loger('error', self.ip+" 资产收集失败 "+str(e))
            conn.close_conn()
            return "failed"
