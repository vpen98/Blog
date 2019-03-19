from django.shortcuts import render,redirect
from django.urls import reverse
from django.template.loader import get_template
from django.http import HttpResponse
from datetime import datetime
from django.utils import timezone
from user.models import User, Article, Review
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # 文章分页
import hashlib # 导入哈希库


global massage
massage = []
# 加密
def take_md5(content):
    hash = hashlib.md5() # 创建hash加密实例
    hash.update(content.encode("utf-8"))  # hash加密
    result = hash.hexdigest() # 获取加密结果
    return result

# 注册
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # 判断输入是否为空
        if username and password1 and password2:
            usernamefilter = User.objects.filter(username=username)
            # 判断账号是否存在
            if len(usernamefilter) > 0:
                return render(request,'user_login/register.html', {'massage':"帐号已存在！"})
            else:
                # 判断输入的密码是否相等
                if password1 != password2:
                    return render(request,'user_login/register.html', {'massage':"密码不一样！"})
                else:
                    # 加密
                    password = take_md5(password1)
                    time = datetime.now()
                    # 写入数据表
                    User.objects.create(username = username, password = password, register_time = time)
                    return redirect('/login/',{'massage':"注册成功"})
        else:
            return render(request,'user_login/register.html',{'massage':'填完！'})
    return render(request,'user_login/register.html')


# 登录
def login(request):
    if request.method == 'POST':
        username = request.POST['username']  # 获取输入的帐号
        password = request.POST['password']  # 获取输入的密码
        password = take_md5(password)  # 给密码加密
        namefilter = User.objects.filter(username = username, password = password) # 在数据库条件匹配
        # 判断密码是否正确
        if len(namefilter) > 0 :
            nameget = User.objects.get(username = username)
            request.session['is_login'] = True
            request.session['id'] = nameget.id
            return redirect("../")  # 重定向到首页
        else:
            return render(request,'user_login/login.html',{'massage':"账号或密码错误"})  
    return render(request,'user_login/login.html')



# 装饰器 实现先登录后访问
def my_login_required(func):
    def check_login_status(request, *args, **kwargs):
        # 如果在字典里is_login的值为空，返回none
        
        login_status = request.session.get('is_login', None)
        if not login_status:
            return redirect('/login/')       # 如果没有登录返回登录页面
        ret = func(request, *args, **kwargs) # 如果已经登录返回原函数请求页面
        request.session.set_expiry(60*60*5)
        return ret
    return check_login_status


# 主页展示页 实现分页
def homepage(request):
    article_list = Article.objects.all() # 获取所有文章
    paginator = Paginator(article_list, 5)  # 实例化一个分页对象, 每页显示5个
    page = request.GET.get('page')      # 从URL通过get页码，如?page=3
    articles = paginator.get_page(page)  # 获取某页对应的记录
    now = timezone.now() # 获取当前时间
    login_status = request.session.get('is_login', None)
    return render(request,'homepage.html',{'articles':articles, "time":now,'login_status':login_status})


# 先登录 发布文章的视图
@my_login_required
def postarticle(request):
    if request.method == "POST":
        title = request.POST["title"]     # 获取输入的标题
        content = request.POST["content"] # 获取输入的内容
        # 获取当前登录的人的id
        id_author = request.session.get('id',None) 
        # 选择当前发布文章的人，外键pub_author需选择User
        pub_author = User.objects.get(id=id_author) # 获取当前登录者数据库的记录
        Article.objects.create(title=title, content=content, pub_author=pub_author)
        return redirect('../') # 发表文章完后重定向回到首页
    return render(request,'postarticle.html')


# 文章内容页
def showpage(request, id):
    try:
        articles = Article.objects.get(id=id) # 将url传来的参数id用来找到对应的文章
        reviews = articles.review.all()       # 一对多，由一找多,将当前文章所有的评论全部找出，review是外键定义的related_name
        review_number = reviews.count()      # 当前文章的评论数 
        Article.objects.filter(id=id).update(review_number=review_number)
        if articles != None:  
            return render(request, "showpage.html",{'articles':articles,'reviews':reviews})
        
    except:
        return redirect('/')
    
# 评价文章
@my_login_required
def article_review(request,id,pk):
    if request.method == "POST":
        
        '''
        由多找一，通过当前id获取当前评论文章的所有字段
        articleid = Article.objects.get(id=id)
        通过外键pub_author找到主表的字段；pub_author_id对应的是主表唯一的id
        userid = User.objects.get(id=articleid.pub_author_id)
        '''
        comment = request.POST["comment"]
        id_author = request.session.get('id',None)
        comment_uesr = User.objects.get(id=id_author)
        # 选择当前评论的文章，外键的article需选择Article
        # 就是多对一，一是必须是一个完整的模型
        review_article = Article.objects.get(id=pk)
        Review.objects.create(comment_uesr=comment_uesr.nicename, comment=comment, article=review_article)
        return redirect('../') # 重定向到上一页
    return render(request, 'postreview.html')