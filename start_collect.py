# -*- coding: utf-8 -*-
# @Time    : 2018/4/11 下午5:47
# @Author  : 大兵

import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_cmdb.settings")
django.setup()

from collect.make_data import Data
from repository.models import  Server,Asset,Disk_info
from collect.test_log import Loger

def save_data():
    # 取得连接信息等
    servers = Server.objects.exclude(port=3389).exclude(hostname__icontains="RDS")

    for s in servers:
        hostname = s.hostname
        ip = s.remote_ip
        username = s.username
        port = s.port
        password = s.password

        # 收集数据
        ret = Data(ip=ip,username=username,port=port,password=password).make_data()
        print("============================================================================")
        print(hostname)
        print(ret)
        if ret == "failed":
            Loger('error',ip+" "+hostname+"连接失败,未修改资产")
            continue
        if s.assets_id:
            # 更新资产
            asset_id = Server.objects.filter(id=s.id)[0].assets_id
            asset = Asset.objects.filter(id=asset_id).update(
                release=ret["sys_version"], kernel_version=ret["kernel"], cpu_type=ret["cputype"],
                cpu_nums=ret["cpunum"], mem=ret["mem"], swap=ret["swap"]
            )

            Loger('info',ip+" "+ret["hostname"]+"更新资产成功！")
        else:
            # 首次添加资产
            asset = Asset.objects.create(
                release=ret["sys_version"],kernel_version=ret["kernel"],cpu_type=ret["cputype"],
                cpu_nums=ret["cpunum"],mem=ret["mem"],swap=ret["swap"]
            )

            s.assets_id = asset.id

            Loger('info', ip+" "+ret["hostname"] + "首次添加资产成功！")

        s.self_ip = ret["ip"]
        s.save()

        disk_names = s.disk_info.filter(server_disk=s.id)

        disk_arr = []
        for k,v in ret['disk'].items():
            disk_arr.append(k)

        for d_name in disk_names:
            disks = Disk_info.objects.filter(id=d_name.id)
            for d in disks:
                if d.name in disk_arr:
                    d.size = ret['disk'][d.name]
                    d.save()
                    disk_arr.remove(d.name)
            Loger('info', ip+" "+ret["hostname"] + "更新磁盘成功！")

        # 添加新的磁盘
        if disk_arr:
            for i in disk_arr:
                disk_info = Disk_info.objects.create(name=i,size=ret['disk'][i])
                s.disk_info.add(disk_info)
            Loger('info', ip+" "+ret["hostname"] + "首次添加磁盘成功！")

save_data()