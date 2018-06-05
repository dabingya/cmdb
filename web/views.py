from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from django.views import View
from django.db.models import Q
from pure_pagination import Paginator,EmptyPage,PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from web.forms import ServerAddForm,AccountAddForm,LoginForm,AddDomainForm,AddConnectForm
from repository.models import Server,IDC,Team,Account,Domain,Connect
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class LoginView(View):
    """
    登录
    """
    def get(self,request):

        return render(request,'login.html',{})

    def post(self,request):

        username = request.POST.get("username","")
        password = request.POST.get("password","")

        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(username=username,password=password)

            if user:
                # 登录
                login(request,user)

                return redirect('/index/')
            else:
                return render(request,'login.html',{
                    "login_form": login_form,
                    "err": "用户名或者密码错误",
            })
        else:
            return render(request,'login.html',{
                "err": "请输入用户名或者密码",
                "login_form": login_form,
            })

class Lgout(View):
    """
    退出登录
    """
    def get(self,request):
        print("aaaaa")
        from django.db import connection
        cursor = connection.cursor()
        skey = request.session.session_key
        sql = "delete from django_session where session_key=\'" + skey +"\'"
        print(sql)
        cursor.execute(sql)
        return redirect('/login')


class IndexView(LoginRequiredMixin,View):
    """
    平台首页
    """
    def get(self,request):

        return render(request,'index.html',{})


class ServerView(LoginRequiredMixin,View):
    """
    服务器首页
    """
    @csrf_exempt
    def get(self,request):
        # 获取所有的业务线
        team = Team.objects.all()

        status = request.GET.get("status")
        if status == "1":
            tips = "添加成功!"
        elif status == "2":
            tips = "更新成功!"
        else:
            tips = None

        # 搜索
        category = request.GET.get('category',"0")
        keyword = request.GET.get('keyword',"")

        if category == "0":
            all_server = Server.objects.filter(
                Q(hostname__icontains=keyword)|Q(remote_ip__icontains=keyword)|Q(self_ip__icontains=keyword))
        else:
            all_server = Server.objects.filter(team_id=category).filter(
                Q(hostname__icontains=keyword)|Q(remote_ip__icontains=keyword)|Q(self_ip__icontains=keyword))

        # 分页
        count = all_server.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger :
            page = 1

        s = Paginator(all_server, 10, request=request)
        servers = s.page(page)

        return render(request,'server.html',{
            "all_server": servers,
            "c_page": "server",
            "tips":tips,
            "count":count,
            "team":team,
            "category": category,
            "keyword": keyword,
        })


class ServerDetailView(LoginRequiredMixin,View):
    """
    服务器详情页
    """
    def get(self,request,id):

        try:
            server = Server.objects.filter(id=id)[0]


            return render(request, 'server-detail.html', {
                "server": server,
                "c_page": "server",
            })

        except Exception as e:

            return render(request,'error.html')


class ServerEditView(LoginRequiredMixin,View):
    """
    编辑详细
    """
    def get(self,request,idd):
        try:
            # 获取所有的机房
            idc = IDC.objects.all()
            # 获取所有的业务线
            team = Team.objects.all()
            # 获取所有的账号
            account = Account.objects.all()
            # 获得所属环境
            env_status = Server.env_choices
            # 获得到期时间
            day_choices = Server.day_choices
            # 获得修改的server
            server = Server.objects.filter(id=idd)[0]

            return render(request, 'server-edit.html', {
                "server": server,
                "c_page": "server",
                "idcs": idc,
                "teams": team,
                "accounts": account,
                "envs": env_status,
                "days": day_choices,
            })

        except Exception as e:
            return render(request,'error.html')

    def post(self,request,idd):
        """
        数据验证通过，update数据
        """
        edit_form = ServerAddForm(request.POST)
        if edit_form.is_valid():
            try:
                # 获得用户填写值
                hostname = edit_form.cleaned_data['hostname']
                remote_ip = edit_form.cleaned_data['remote_ip']
                port = edit_form.cleaned_data['port']
                idc_id = edit_form.cleaned_data['idc']
                team_id = edit_form.cleaned_data['team']
                account_id = edit_form.cleaned_data['account']
                username = edit_form.cleaned_data['username']
                password = edit_form.cleaned_data['password']
                price = edit_form.cleaned_data['price']
                senv = edit_form.cleaned_data['env']
                deadtime = edit_form.cleaned_data['deadtime']
                info = edit_form.cleaned_data['info']
                info_secret = edit_form.cleaned_data['info_secret']
                # 更新数据
                Server.objects.filter(id=idd).update(hostname=hostname, remote_ip=remote_ip, port=port,
                                    idc_id=idc_id, team_id=team_id,username=username, password=password,
                                    price=price, env_status=senv, deadtime=deadtime,
                                      info=info, info_sercret=info_secret)

                # 更新account
                if account_id != "0":
                    Server.objects.filter(id=idd).update(account_id=account_id)

                return redirect('/server/?status=2')
            except Exception as e:
                """
                发生错误
                """
                # 获取所有的机房
                idc = IDC.objects.all()
                # 获取所有的业务线
                team = Team.objects.all()
                # 获取所有的账号
                account = Account.objects.all()
                # 获得所属环境
                env_status = Server.env_choices
                # 获得到期时间
                day_choices = Server.day_choices
                server = Server.objects.filter(id=idd)[0]

                return render(request, 'server-edit.html', {
                    "err": "已存在此主机名服务器",
                    "server": server,
                    "idcs": idc,
                    "c_page": "server",
                    "teams": team,
                    "accounts": account,
                    "envs": env_status,
                    "days": day_choices,
                    "addserver_form": edit_form,
                    "error": edit_form.errors,
                })

        else:
            """
            数据验证不通过，重新填写
            """
            # 获取所有的机房
            idc = IDC.objects.all()
            # 获取所有的业务线
            team = Team.objects.all()
            # 获取所有的账号
            account = Account.objects.all()
            # 获得所属环境
            env_status = Server.env_choices
            # 获得到期时间
            day_choices = Server.day_choices
            server = Server.objects.filter(id=idd)[0]

            return render(request, 'server-edit.html', {
                "server": server,
                "idcs": idc,
                "teams": team,
                "c_page": "server",
                "accounts": account,
                "envs": env_status,
                "days": day_choices,
                "addserver_form": edit_form,
                "error": edit_form.errors,
            })



class AddServerView(LoginRequiredMixin,View):
    """
    新增服务器
    """

    def get(self,request):
        # 获取所有的机房
        idc = IDC.objects.all()
        # 获取所有的业务线
        team = Team.objects.all()
        # 获取所有的账号
        account = Account.objects.all()
        # 获得所属环境
        env_status = Server.env_choices
        # 获得到期时间
        day_choices = Server.day_choices


        return render(request,'server-add.html',{
            "idcs": idc,
            "c_page": "server",
            "teams": team,
            "accounts": account,
            "envs": env_status,
            "days": day_choices,
        })

    def post(self,request):
        addserver_form = ServerAddForm(request.POST)
        if addserver_form.is_valid():

            try:
                # 获得用户填写值
                hostname = addserver_form.cleaned_data['hostname']
                remote_ip = addserver_form.cleaned_data['remote_ip']
                port = addserver_form.cleaned_data['port']
                idc_id = addserver_form.cleaned_data['idc']
                team_id = addserver_form.cleaned_data['team']
                account_id = addserver_form.cleaned_data['account']
                username = addserver_form.cleaned_data['username']
                password = addserver_form.cleaned_data['password']
                price = addserver_form.cleaned_data['price']
                senv = addserver_form.cleaned_data['env']
                deadtime = addserver_form.cleaned_data['deadtime']
                info = addserver_form.cleaned_data['info']
                info_secret = addserver_form.cleaned_data['info_secret']

                # 更新account
                if account_id != "0":
                    Server.objects.create(hostname=hostname, remote_ip=remote_ip, port=port, idc_id=idc_id,
                                          team_id=team_id,
                                          username=username, account_id=account_id, password=password, price=price,
                                      env_status=senv, deadtime=deadtime, info=info, info_sercret=info_secret)
                else:
                    Server.objects.create(hostname=hostname, remote_ip=remote_ip, port=port, idc_id=idc_id,
                                          team_id=team_id,
                                          username=username, password=password, price=price,
                                          env_status=senv, deadtime=deadtime, info=info, info_sercret=info_secret)

                return redirect('/server/?status=1')


            except Exception as e:
                print(e)
                # 获取所有的机房
                idc = IDC.objects.all()
                # 获取所有的业务线
                team = Team.objects.all()
                # 获取所有的账号
                account = Account.objects.all()
                # 获得所属环境
                env_status = Server.env_choices
                # 获得到期时间
                day_choices = Server.day_choices

                return render(request, 'server-add.html', {
                    "err":"已存在此主机名服务器",
                    "idcs": idc,
                    "teams": team,
                    "c_page": "server",
                    "accounts": account,
                    "envs": env_status,
                    "days": day_choices,
                    "addserver_form": addserver_form,
                    "error": addserver_form.errors,
                })


        else:
            # 获取所有的机房
            idc = IDC.objects.all()
            # 获取所有的业务线
            team = Team.objects.all()
            # 获取所有的账号
            account = Account.objects.all()
            # 获得所属环境
            env_status = Server.env_choices
            # 获得到期时间
            day_choices = Server.day_choices

            return render(request,'server-add.html',{
                "idcs": idc,
                "teams": team,
                "accounts": account,
                "c_page": "server",
                "envs": env_status,
                "days": day_choices,
                "addserver_form": addserver_form,
                "error": addserver_form.errors,
            })


class AccountView(LoginRequiredMixin,View):
    @csrf_exempt
    def get(self,request):

        # 获取添加或更新状态
        status = request.GET.get("status")
        if status == "1":
            tips = "添加成功!"
        elif status == "2":
            tips = "更新成功!"
        else:
            tips = None

        # 获取搜索类别及关键字
        category = request.GET.get('category', "all")
        keyword = request.GET.get('keyword', "")

        accounts = Account.objects.all()
        if category == "all":
            accounts = accounts.filter(Q(name__icontains=keyword)|Q(info__icontains=keyword))
        else:
            accounts = accounts.filter(belong_to__icontains=category).filter(Q(name__icontains=keyword)|Q(info__icontains=keyword))

        count = accounts.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        s = Paginator(accounts, 10, request=request)
        accounts = s.page(page)

        account_choices = Account.account_choices
        return render(request, 'account.html',{
            "c_page": "account",
            "tips": tips,
            "accounts": accounts,
            "count": count,
            "account_choices":account_choices,
            "category": category,
            "keyword": keyword,
        })


class AddAccountView(LoginRequiredMixin,View):
    def get(self,request):
        # 获取所有的账号类型
        account_choices = Account.account_choices

        return render(request,'account-add.html',{
            "c_page": "account",
            "account_choices": account_choices,
        })
    def post(self,request):
        addaccount_form = AccountAddForm(request.POST)

        # 验证填写值
        if addaccount_form.is_valid():

            name = addaccount_form.cleaned_data['name']
            password = addaccount_form.cleaned_data['password']
            type = addaccount_form.cleaned_data['account_type']
            url = addaccount_form.cleaned_data['url']
            info = addaccount_form.cleaned_data['info']

            Account.objects.create(name=name,password=password,belong_to=type,info=info,url=url)

            return redirect('/account/?status=1')
        else:
            # 获取所有的账号类型
            account_choices = Account.account_choices

            return render(request,'account-add.html',{
                "c_page": "account",
                "account_choices": account_choices,
                "addaccount_form": addaccount_form,
                "error": addaccount_form.errors,
            })


class AccountEditView(LoginRequiredMixin,View):
    def get(self,request,id):
        account_choices = Account.account_choices
        try:
            """
            判断是否存在此id的账号
            """
            account = Account.objects.filter(id=id)[0]
            return render(request,'account-edit.html',{
                "c_page": "account",
                "account_choices": account_choices,
                "account": account,
            })

        except Exception as e:
            return render(request, 'error.html')
    def post(self,request,id):

        addaccount_form = AccountAddForm(request.POST)
        # 验证填写值
        if addaccount_form.is_valid():
            name = addaccount_form.cleaned_data['name']
            password = addaccount_form.cleaned_data['password']
            type = addaccount_form.cleaned_data['account_type']
            url = addaccount_form.cleaned_data['url']
            info = addaccount_form.cleaned_data['info']

            account = Account.objects.filter(id=id)
            account.update(name=name,password=password,belong_to=type,info=info,url=url)

            return redirect('/account/?status=2')
        else:
            # 获取所有的账号类型
            account_choices = Account.account_choices

            return render(request,'account-add.html',{
                "c_page": "account",
                "account_choices": account_choices,
                "addaccount_form": addaccount_form,
                "error": addaccount_form.errors,
            })


class DomainView(LoginRequiredMixin,View):
    @csrf_exempt
    def get(self, request):

        # 获取添加或更新状态
        status = request.GET.get("status")
        if status == "1":
            tips = "添加成功!"
        elif status == "2":
            tips = "更新成功!"
        else:
            tips = None

        # 获取搜索类别及关键字
        keyword = request.GET.get('keyword', "")

        domains = Domain.objects.all().filter(Q(name__icontains=keyword) | Q(info__icontains=keyword))

        count = domains.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        s = Paginator(domains, 10, request=request)
        domains = s.page(page)

        return render(request, 'domain.html', {
            "c_page": "domain",
            "tips": tips,
            "count": count,
            "keyword": keyword,
            "domains": domains,
        })


class AddDomainView(LoginRequiredMixin,View):
    """
    新增域名
    """
    def get(self,request):
        # 获取所有的账号
        accounts = Account.objects.all()

        return render(request,'domain-add.html',{
            "c_page": "domain",
            "accounts": accounts,
        })
    def post(self,request):

        adddomain_form = AddDomainForm(request.POST)
        if adddomain_form.is_valid():
            # 填写正确
            d_name = adddomain_form.cleaned_data['d_name']
            ip = adddomain_form.cleaned_data['resolution']
            account = adddomain_form.cleaned_data['account']
            price = adddomain_form.cleaned_data['price']
            deadtime = adddomain_form.cleaned_data['date']
            info = adddomain_form.cleaned_data['info']

            Domain.objects.create(name=d_name,resolution=ip,account_id=account,price=price,datetime=deadtime,info=info)
            return redirect('/domain/?status=1')

        else:
            #填写不正确
            accounts = Account.objects.all()

            return render(request, 'domain-add.html', {
                "c_page": "domain",
                "accounts": accounts,
                "adddomain_form": adddomain_form,
                "error": adddomain_form.errors,
            })


class EditDomainView(LoginRequiredMixin,View):
    """
    修改域名信息
    """
    def get(self,request,id):
        domain_info = Domain.objects.filter(id=id)[0]
        accounts = Account.objects.all()
        return render(request,'domain-edit.html',{
            "d_info": domain_info,
            "c_page": "domain",
            "accounts": accounts,
        })
    def post(self,request,id):
        accounts = Account.objects.all()

        adddomain_form = AddDomainForm(request.POST)
        if adddomain_form.is_valid():

            d_name = adddomain_form.cleaned_data['d_name']
            ip = adddomain_form.cleaned_data['resolution']
            account = adddomain_form.cleaned_data['account']
            price = adddomain_form.cleaned_data['price']
            deadtime = adddomain_form.cleaned_data['date']
            info = adddomain_form.cleaned_data['info']

            Domain.objects.filter(id=id).update(resolution=ip, account_id=account, price=price, datetime=deadtime,
                                                info=info)

            return redirect('/domain/?status=2')
        else:
            domain_info = Domain.objects.filter(id=id)[0]

            return render(request, 'domain-edit.html', {
                "c_page": "domain",
                "accounts": accounts,
                "d_info": domain_info,
                "adddomain_form": adddomain_form,
                "error": adddomain_form.errors,
            })


class ConnectView(LoginRequiredMixin,View):
    def get(self,request):

        # 获取添加或更新状态
        status = request.GET.get("status")
        if status == "1":
            tips = "添加成功!"
        elif status == "2":
            tips = "更新成功!"
        else:
            tips = None

        # 获取所有的联系人
        persons = Connect.objects.all()

        # 搜索
        keyword = request.GET.get('keyword', "")
        persons = persons.filter(Q(name__icontains=keyword)|Q(mobile__icontains=keyword)|Q(tel__icontains=keyword)|Q(info__icontains=keyword))
        # 分页
        count = persons.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        s = Paginator(persons, 10, request=request)
        persons = s.page(page)

        return render(request, 'connect.html',{
            "c_page": "connect",
            "persons": persons,
            "count": count,
            "tips": tips,
            "keyword": keyword,
        })


class AddConnectView(LoginRequiredMixin,View):
    """
    新增联系人
    """
    def get(self,request):

        return render(request,'connect-add.html',{
            "c_page": "connect",
        })
    def post(self,request):
        addconnect_form = AddConnectForm(request.POST)

        # 判断新增联系人填写是否正确
        if addconnect_form.is_valid():
            # 处理数据
            username = addconnect_form.cleaned_data['username']
            mobile = addconnect_form.cleaned_data['mobile']
            tel = addconnect_form.cleaned_data['tel']
            info = addconnect_form.cleaned_data['info']

            Connect.objects.create(name=username,mobile=mobile,tel=tel,info=info)
            return redirect('/connect/?status=1')
        else:

            return render(request,'connect-add.html',{
                "c_page": "connect",
                "error": addconnect_form.errors,
                "addconnect_form": addconnect_form,
            })


class EditConnectView(LoginRequiredMixin,View):
    """
    编辑联系人
    """
    def get(self,request,id):

        connect_info = Connect.objects.filter(id=id)[0]

        return render(request, 'connect-edit.html', {
            "c_info": connect_info,
            "c_page": "connect",
        })

    def post(self,request,id):
        addconnect_form = AddConnectForm(request.POST)

        if addconnect_form.is_valid():
            # 填写正确 修改
            username = addconnect_form.cleaned_data['username']
            mobile = addconnect_form.cleaned_data['mobile']
            tel = addconnect_form.cleaned_data['tel']
            info = addconnect_form.cleaned_data['info']

            Connect.objects.filter(id=id).update(name=username, mobile=mobile, tel=tel, info=info)

            return redirect('/connect/?status=2')
        else:
            # 填写错误
            connect_info = Connect.objects.filter(id=id)[0]
            return render(request, 'connect-edit.html', {
                "c_page": "connect",
                "error": addconnect_form.errors,
                "c_info": connect_info,
                "addconnect_form": addconnect_form,
            })




class UpdateDataView(View):
    def get(self,request):
        """
        更新数据
        """
        import start_collect

        start_collect.save_data()
        return HttpResponse("更新成功")