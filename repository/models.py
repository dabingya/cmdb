from datetime import datetime
from django.db import models

# 用户信息
class UserProfile(models.Model):
    name = models.CharField(u'姓名', max_length=32)
    email = models.EmailField(u'邮箱')
    phone = models.CharField(u'座机', max_length=32)
    mobile = models.CharField(u'手机', max_length=32)

    class Meta:
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.name


# 服务器信息
class Server(models.Model):
    day_choices = (
        ("0",0),("1", 1), ("2", 2),("3", 3),("4", 4), ("5", 5), ("6", 6),
        ("7", 7), ("8", 8), ("9", 9), ("10", 10), ("11", 11), ("12", 12), ("13", 13), ("14", 14), ("15", 15),
        ("16", 16), ("17", 17), ("18", 18), ("19", 19), ("20", 20), ("21", 21), ("22", 22), ("23", 23),
        ("24", 24), ("25", 25), ("26", 26), ("27", 27), ("28", 28), ("29", 29), ("30", 30), ("31", 31)
    )
    env_choices = (
        ("test","测试环境"),
        ("prod","生产环境"),
        ("preprod","预生产环境"),
        ("base","基础环境"),
    )
    update_choices = (
        ("0", "未更新"),
        ("1", "已更新"),
        ("2", "更新失败"),
    )
    hostname = models.CharField(verbose_name="主机名",max_length=40,unique=True)
    remote_ip = models.CharField(verbose_name="远程连接IP",max_length=20)
    port = models.IntegerField(verbose_name="连接端口",default=22)
    self_ip = models.CharField(verbose_name="内网ip",max_length=200,blank=True,null=True)
    idc = models.ForeignKey("IDC",verbose_name="所属机房")
    team = models.ForeignKey("Team",verbose_name="所属业务线")
    account = models.ForeignKey("Account",verbose_name="所属账号",blank=True,null=True)
    username = models.CharField(verbose_name="用户名",default="root",max_length=20)
    password = models.CharField(verbose_name="密码",max_length=50)
    price = models.FloatField(verbose_name="价格",default=0)
    env_status = models.CharField(verbose_name="所属环境",choices=env_choices,max_length=20,default="测试")
    deadtime = models.IntegerField(choices=day_choices,default=0,verbose_name="到期时间")
    info = models.CharField(max_length=200, verbose_name="备注",blank=True,null=True)
    info_sercret = models.TextField(default="请输入密码信息", max_length=400, verbose_name="登陆密码信息",blank=True,null=True)
    assets = models.OneToOneField("Asset",verbose_name="资产信息",related_name="assets",blank=True,null=True)
    disk_info = models.ManyToManyField("Disk_info",verbose_name="硬盘信息",related_name="server_disk",blank=True)
    update_status = models.CharField(verbose_name="更新状态",choices=update_choices,max_length=40,default="未更新")

    class Meta:
        verbose_name_plural = "服务器表"

    def __str__(self):
        return self.hostname


# 资产信息
class Asset(models.Model):
    # 系统版本
    release = models.CharField(verbose_name="系统版本",max_length=50,blank=True,null=True)
    kernel_version = models.CharField(verbose_name="内核版本",max_length=50,blank=True,null=True)
    # cpu
    cpu_type = models.CharField(verbose_name="CPU型号",max_length=50,blank=True,null=True)
    cpu_nums = models.IntegerField(verbose_name="CPU个数",default=0)
    # 内存
    mem = models.CharField(verbose_name="内存",max_length=50,blank=True,null=True)
    swap = models.CharField(verbose_name="swap",max_length=50,blank=True,null=True)

    class Meta:
        verbose_name_plural = "资产表"

    def __str__(self):
        return self.release + "资产信息"


class Disk_info(models.Model):
    # 硬盘信息 名称与大小
    name = models.CharField(verbose_name="磁盘名称",max_length=10,blank=True,null=True)
    size = models.CharField(verbose_name="磁盘大小",max_length=50,blank=True,null=True)

    class Meta:
        verbose_name_plural = "硬盘信息"

    def __str__(self):
        return self.name + "硬盘信息"



# 业务线
class Team(models.Model):
    name = models.CharField(verbose_name="业务线名称",max_length=10)
    create_at = models.DateField(default=datetime.now().strftime('%Y-%m-%d'),verbose_name="创建时间")

    class Meta:
        verbose_name = "业务线表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 机房信息  含有物理机 阿里云
class IDC(models.Model):
    name = models.CharField(verbose_name="机房名称",max_length=10)
    romm_pos = models.CharField(verbose_name="机房位置",max_length=50,blank=True,null=True)
    cabinet_pos = models.CharField(verbose_name="机柜位置",max_length=50,blank=True,null=True)
    create_at = models.DateField(default=datetime.now().strftime('%Y-%m-%d'),verbose_name="创建时间")

    class Meta:
        verbose_name = "机房表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 资产变更记录



# 第三方账号  内部账号
class Account(models.Model):
    account_choices = (
        ("aly", "阿里云"),
        ("llht", "流量后台"),
        ("beian", "备案"),
        ("yxgl", "邮箱管理"),
        ("domian", "域名"),
        ("qyqq", "企业QQ"),
        ("dxpt", "短信平台"),
        ("internet", "网络"),
        ("other", "其他")
    )
    name = models.CharField(verbose_name="账号",max_length=50)
    password = models.CharField(verbose_name="密码",max_length=50)
    belong_to = models.CharField(max_length=50, default="阿里云", choices=account_choices, verbose_name="账号类别")
    url = models.URLField(verbose_name="登录地址",max_length=100)
    info = models.CharField(verbose_name="备注信息",max_length=200)


# 域名管理
class Domain(models.Model):
    name = models.CharField(max_length=50,verbose_name="域名")
    resolution = models.CharField(max_length=50,verbose_name="解析IP")
    account = models.ForeignKey(Account, verbose_name="所属账号")
    price = models.IntegerField(verbose_name="价格")
    datetime = models.DateField(default=datetime.now().strftime('%Y-%m-%d'),verbose_name="到期时间")
    info = models.CharField(max_length=200,verbose_name="备注")

    class Meta:
        verbose_name = "域名管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 联系人管理
class Connect(models.Model):
    name = models.CharField(max_length=50,verbose_name="姓名")
    mobile = models.CharField(max_length=20,verbose_name="手机号码",blank=True,null=True)
    tel = models.CharField(max_length=20,verbose_name="固定电话",blank=True,null=True)
    info = models.CharField(max_length=200,verbose_name="备注",blank=True,null=True)

    class Meta:
        verbose_name = "联系人管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

