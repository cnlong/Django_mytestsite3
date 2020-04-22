from django.shortcuts import render,redirect
from django.template import loader,RequestContext
from django.http import HttpResponse
from booktest.models import *
from PIL import Image, ImageDraw, ImageFont
from django.urls import reverse
from django.utils.six import BytesIO
import random
# Create your views here.


def login_required(view_func):
    """是否登录判断装饰器"""
    def wrapper(request,*args, **kwargs):
        # 判断用户是否登录
        if request.session.has_key('islogin'):
            # 用户已登录，跳转到密码修改页面
            return view_func(request, *args, **kwargs)
        else:
            return redirect('/login/')
    return wrapper

def index(request):
    # # 1.加载模板文件，获取一个模板对象
    # temp = loader.get_template('booktest/index.html')
    # # 2. 定义模板上下文，给模板文件传递数据(字典)
    # context = {}
    # # 3.模板渲染，产生一个替换后的html内容
    # result = temp.render(context)
    # # 4.返回应答
    # return HttpResponse(result)
    # 通过自带的render方法，简化上述的方法
    return render(request, 'booktest/index.html', {})


def index2(request):
    return render(request, 'booktest/index2.html', {})


def temp_var(request):
    """模板变量"""
    my_dict = {'title': '字典键值'}
    my_list = [1, 2, 3]
    book = BookInfo.objects.get(id=1)
    context = {'my_dict': my_dict, 'my_list': my_list, 'book': book}
    return render(request, 'booktest/temp_var.html', context)


def temp_targs(request):
    """模板标签"""
    book = BookInfo.objects.all()
    return render(request, 'booktest/temp_targs.html', {'book': book})


def temp_filter(request):
    """模板标签"""
    book = BookInfo.objects.all()
    return render(request, 'booktest/temp_filter.html', {'book': book})


def temp_inherit(request):
    """模板继承"""
    return render(request, 'booktest/child.html')


def html_escape(request):
    return render(request, 'booktest/html_escape.html', {'content': '<h1>hello</h1>'})


def login(request):
    """显示登录页面"""
    # 判断用户是否登录
    if request.session.has_key('islogin'):
        # 用户已登录，跳转到密码修改页面
        return redirect('/change_pwd')
    else:
        # 用户未登录
        # 判断是否有cookie。从cookie中获取已输入的用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
        else:
            username = ''
        return render(request, 'booktest/login.html', {'username': username})


def login_check(request):
    """登录校验视图"""
    # request.POST 保存的是post方式提交的参数,QueryDict类型数据，类似于字典
    # request.GET 保存的是get方式提交的参数
    # 1.获取提交的用户名和密码
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 获取用户输入验证码
    vcode1 = request.POST.get('vcode')
    # 从session中获取正确的验证码
    vcode2 = request.session.get('verifycode')
    # 进行验证码校验
    if vcode1 != vcode2:
        return redirect("/login/")
    # 获取记住按钮的值
    remember = request.POST.get('remember')
    # 2.进行登录校验
    # 实际开发：使用用户名和密码查找数据库
    # 模拟admin 123
    if username == 'admin' and password == '123':
        response = redirect('/change_pwd')
        # 用户名密码正确
        # 跳转到密码修改页面
        # 判断记住按钮的值
        if remember == 'on':
            # 设置cookie(username)，过期时间为1周
            response.set_cookie('username', username, max_age=7*24*3600)
        # 记住用户的登录状态
        # 只有session中有islogin，就认为该用户已经登录
        request.session['islogin'] = True
        # 记住登录的用户名
        request.session['username'] = username
        return response  # redirect('/index')返回发就是一个HttpResponseRedirect对象，就是HttpResponse的子类
    else:
        # 用户名密码错误
        return redirect('/login/')


@login_required
def change_pwd(request):
    """显示修改密码页面"""
    # # 进行用户是否登录的判断
    # if not request.session.has_key('islogin'):
    #     # 未登录返回到登录页
    #     return redirect('/login/')
    return render(request, 'booktest/change_pwd.html')


@login_required
def change_pwd_action(request):
    """模拟修改密码处理"""
    # # 进行用户是否登录的判断
    # if not request.session.has_key('islogin'):
    #     # 未登录返回到登录页
    #     return redirect('/login/')
    # 1.获取新密码
    pwd = request.POST.get('pwd')
    # 获取用户名
    username = request.session.get('username')
    # 2.实际开发的时候，修改对应数据库中的内容
    # 3.返回一个应答
    return HttpResponse('%s修改密码为:%s'% (username, pwd))


def verify_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)  #用rgb方式定义颜色
    width = 100
    height = 25
    # 创建画面对象，并设置宽高
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):  # 循环遍历100次，在画面上添加噪点
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)   # 指定在哪个点画，画的颜色是什么
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('arial.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证（对比用户输入的验证码对不对）
    request.session['verifycode'] = rand_str
    # 内存文件操作
    buf = BytesIO()
    # 将图片（im）保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


def url_reverse(request):
    """url反向解析"""
    return render(request, 'booktest/url_reverse.html')


def show_args(request, a, b):
    return HttpResponse(str(a) + ":" + str(b))


def test_reverse(request):
    """函数内部重定向使用url反向解析"""
    return redirect(reverse('index'))