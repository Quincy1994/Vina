# coding=utf-8
from django.shortcuts import render, render_to_response
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from algorithm import *
from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.contrib.auth.models import User
from thesite.models import Userprofile
import os, tempfile
from django.core.servers.basehttp import FileWrapper
from django.http import JsonResponse
import shutil
homeindex='/home/fen/'

class UserForm(forms.Form):    # 登陆页面用户表单
    username = forms.CharField(label='用户名：',  error_messages={'required': '请输入用户名'}, max_length=100)
    password = forms.CharField(label='密码：', error_messages={'required': '请输入密码'}, widget=forms.PasswordInput())


def login(request):     # 登陆页面
    if request.user.is_authenticated():
        massage = '你已经登陆'
        back = 'index/'
        return render_to_response('redirect.html', {'massage': massage, 'back': back})
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    user_login(request, user)
                    return HttpResponseRedirect('/index/%s' % user.username)
                else:
                    print "Your account has been disabled!"
            else:
                return render_to_response('login.html', RequestContext(request, {'password_is_wrong': True}))
    else:
            uf = UserForm()
    return render_to_response('login.html', {'uf': uf})


class SignForm(forms.Form):     # 用户表单
    username = forms.CharField(label='用户名：', max_length=100)
    password = forms.CharField(label='密码：', widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件：')


def register(request):  # 注册页
    if request.method == "POST":
        uf = SignForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            email = uf.cleaned_data['email']
            if User.objects.exclude(pk=request.user.pk).filter(username=username).exists():
                return render_to_response('register.html', RequestContext(request, {'password_is_wrong': True}))
            else:
                # User._meta.get_field('username')._unique = False
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                os.mkdir(homeindex+"demo/static/dv/%s"%username)
                os.mkdir(homeindex+"demo/data/%s"%username)

                return HttpResponseRedirect('/login/')
    else:
        uf = SignForm()
    return render_to_response('register.html', {'uf': uf})


class DataForm(forms.Form):
    username = forms.CharField()
    sourcefile = forms.FileField()
    labelfile = forms.FileField()
    algo = forms.CharField()
    parameter = forms.CharField()


class OneComAlphaException(Exception):
    def __int__(self, alpha):
        Exception.__init__(self)
        self.alpha = alpha


def index(request):     # 主页
    df = DataForm(request.POST, request.FILES)
    if not request.user.is_authenticated():
        massage = '请登陆'
        back = 'login/'
        return render_to_response('redirect.html', {'massage': massage, 'back': back})
    if request.POST:
        if request.user.is_authenticated():
            user = request.user
            user = request.user
            if os.path.exists(homeindex+"demo/static/dv/%s/ok" % user):
                shutil.rmtree(homeindex+"demo/static/dv/%s/ok" % user)
            if os.path.exists(homeindex+"demo/static/dv/%s" % user):
                shutil.rmtree(homeindex+"demo/static/dv/%s" % user)
            os.mkdir(homeindex+"demo/static/dv/%s" % user)
            if os.path.exists(homeindex+"demo/data/%s" % user):
                shutil.rmtree(homeindex+"demo/data/%s" % user)
            os.mkdir(homeindex+"demo/data/%s" % user)
            os.mkdir(homeindex+"demo/static/dv/%s/ok" % user)
            algo = request.POST['algo']
            sourcefile = request.FILES['sourcefile']
            labelname = None
            try:
                labelfile = request.FILES['labelfile']
                labelname = request.FILES['labelfile'].name
            except:
                    labelfile = None
            try:
                profile = request.user.userprofile
            except Userprofile.DoesNotExist:
                profile = Userprofile(user=request.user)
            profile.user_id = user.id
            profile.file = sourcefile
            profile.labelfile = labelfile
            profile.save()
            user.save()
            fileroot = request.FILES['sourcefile'].name
            parameter = None
            algo = int(algo)
            if algo == 3:
                parameter = request.POST['k-parameter']
            if algo == 4:
                parameter = request.POST['parameter']
            sfile = homeindex+'demo/data/'+fileroot
            file=homeindex+'demo/data/%s/'%user+fileroot
            shutil.copy(sfile,file)
            os.remove(sfile)
            try:
                labelfile1 = homeindex+'demo/data/'+labelname
                labelfile=homeindex+'demo/data/%s/'%user+labelname
                shutil.copy(labelfile1, labelfile)
                os.remove(labelfile1)
            except:
                labelfile = None
            i1 = GetInfo()
            nodes = i1.Dianshu(file)
            edges = i1.Bianshu(file)
            averageweight = i1.PingjunQz(file)
            result, q, listresult,g= algorithm(algo, file, parameter, labelfile, user)
            if labelfile == None:
               labelresult = result
            else:
                labelresult = numtolabel(labelfile, result)
            q = round(q, 3)
            averageweight = round(averageweight, 3)
            communities = i1.Comnum(result)
            net_src = "/static/dv/%s/SNA.png" % user
            return render_to_response('SNA-main.html', {
                'nodes': nodes,
                'edges': edges,
                'averageweight': averageweight,
                'communities': communities,
                'net_url': net_src,
                'module': q,
            })
    return render(request, 'SNA-main.html', {"df": df})


def logout(request):       # 登出
    user_logout(request)
    massage = '您已经退出！'
    back = 'login/'
    return render_to_response('redirect.html', {'massage': massage, 'back': back})


def details(request):       # details页面
    if request.user.is_authenticated():
            user = request.user
    filename = homeindex+"demo/static/dv/%s/labeldata.txt" % user
    tag = 0
    if os.path.exists(homeindex+"demo/static/dv/%s/ok" % user):
        tag = 1
    if tag == 0:
        return HttpResponse("please submit source file and algorithm!")
    out = open(filename)
    line = out.readline()
    li = []
    while line:
        line = line.replace('\n', '')
        li.append(line)
        line = out.readline()
    out.close()
    snapicture = "/static/dv/%s/SNA.png" % user
    chart = "/static/dv/%s/chart.png" % user
    if request.POST:
        user = request.user
        com = request.POST['community']
        com = int(com)
        communtiy_picture = "/static/dv/%s/community%d.png" % (user, com)
        re, list, Lin, label = rd(user)
        nodes, edges, density, senter = drawe(Lin, re, list, label, com, user)
        density = round(density, 4)
        senter = round(senter, 4)
        content = {'comm': True,
                   'communtiy_picture': communtiy_picture,
                   "label": label,
                   "nodes": nodes,
                   "edges": edges,
                   "username": user,
                   "density": density,
                   "SNApicture": snapicture,
                   "chart": chart,
                   "senter": senter,
                   "comlabel": li[com-1], }

        return render_to_response('details.html', content)
        # if os.path.exists("/home/ddjian/demo/static/dv/community%s.png"%com):
        #      return render_to_response('details.html', {"label": li, "communtiy_picture": communtiy_picture})
        # re, l, Lin, label=rd()
        # drawe(Lin, re, l, label, com)
    # os.remove("/home/ddjian/demo/static/dv/%s/ok" % user)
    return render_to_response('details.html', {"label": li, "SNApicture": snapicture, "chart": chart, "username": user})


def figure(request):    # figure页面
    if request.user.is_authenticated():
            user = request.user
    nodes=readnodes(user)
    community=readcommunity(user)
    node1=nodes[0]
    node2=nodes[1]
    node3=nodes[2]
    node4=nodes[3]
    node5=nodes[4]
    com1=community[0]
    com2=community[1]
    com3=community[2]
    com4=community[3]
    com5=community[4]
    url_nodecom="/static/dv/%s/com.png"%user
    url_densitycom="/static/dv/%s/dencom.png"%user
    url_center="/static/dv/%s/center.png"%user
    top=readtop(user)
    least=readleast(user)
    top_least= share=[[0 for i in range(2)]for j in range(5)]
    for i in range(0,5,1):
        top_least[i][0]=top[i]
        top_least[i][1]=least[i]
    top1=top_least[0]
    top2=top_least[1]
    top3=top_least[2]
    top4=top_least[3]
    top5=top_least[4]
    if request.POST:
        try:
            strings = request.POST['nodes']
            if not strings == None:
                filename=homeindex+"demo/static/dv/%s/nodes.xls" % user       # 指定要下载的文件路径
                wrapper = FileWrapper(file(filename))
                response = HttpResponse(wrapper, content_type='text/plain')
                response['Content-Length'] = os.path.getsize(filename)
                response['Content-Encoding'] = 'utf-8'
                response['Content-Disposition'] = 'attachment;filename=%s' % filename
                return response
        except:
            strings = request.POST['comm']
            if not strings == None:
                filename = homeindex+"demo/static/dv/%s/communites.xls"%user       # 指定要下载的文件路径
                wrapper = FileWrapper(file(filename))
                response = HttpResponse(wrapper, content_type='text/plain')
                response['Content-Length'] = os.path.getsize(filename)
                response['Content-Encoding'] = 'utf-8'
                response['Content-Disposition'] = 'attachment;filename=%s' % filename
                return response
    return render(request,'figure.html',{"node1":node1,"node2":node2,"node3":node3,"node4":node4,"node5":node5,
    "com1":com1,"com2":com2,"com3":com3,"com4":com4,"com5":com5,
    "url_nodecom":url_nodecom,
    "url_densitycom":url_densitycom,
    "url_center":url_center,
    "top1":top1,"top2":top2,
    "top3":top3,"top4":top4,
    "top5":top5})


def datasample(request):
    username = request.user.username
    return render(request, 'datasample.html', {"username": username})

def datasamplea(request):
    # username = request.user.username
    filename = homeindex+'demo/static/dataset/a.rar'     # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def datasampleb(request):
    # username = request.user.username
    filename = homeindex+'demo/static/dataset/b.rar'     # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def datasamplec(request):
    # username = request.user.username
    filename = homeindex+'demo/static/dataset/c.rar'     # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def datasampled(request):
    # username = request.user.username
    filename = homeindex+'demo/static/dataset/d.rar'     # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def datasamplee(request):
    # username = request.user.username
    filename = homeindex+'demo/static/dataset/e.rar'     # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response

def helppage(request):
    return render(request, 'help.html')


def redirect(request):
    return render(request, 'redirect.html')

def tyr(request):
    if request.user.is_authenticated():
            user = request.user
    url_js="/static/js/drawgraph/%s/graph.js"%user
    return render(request,'tyr.html',{"url_js":url_js})