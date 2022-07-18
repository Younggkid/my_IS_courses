from django.shortcuts import render, redirect
from meals.models import *
from meals.forms import *
import random
import hashlib


# 首页 （包含搜索功能）
# 5.5 黄祖华 首页搜索完善
def index(request):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')
    else:
        most_likes_meal = Meal.objects.filter().order_by("-likes")  # 按点赞数降序排列菜品
        content = {'meal1': most_likes_meal[0], 'meal2': most_likes_meal[1], 'meal3': most_likes_meal[2]}
        return render(request, 'meals/index.html', content)


def search_result(request):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')

    if request.method == 'POST':
        search_text = request.POST.get('search_data')  # 从前端传入了字符串，没有使用表单
        search_text_len = len(search_text)
        if search_text_len == 0:
            content = {'search__result': []}
            return render(request, 'meals/search_result.html', content)
        i = 0
        search_result_list = []  # 该列表用以储存单个字搜索的结果
        search_result_list_len = []  # 该列表用以储存每个字搜索出的结果的数量
        while i < search_text_len:
            search_result_list.append(Meal.objects.filter(name__contains=search_text[i]))
            search_result_list_len.append(len(search_result_list[i]))
            i = i + 1
        i = 1  # 链式搜索第一步较特殊，需从Meal里filter，故单独写第一步
        search_result_list_final = []  # 该列表用以进行链式搜索
        search_result_list_max = max(search_result_list_len)
        search_text_i = search_result_list_len.index(search_result_list_max)
        search_result_list_final.append(Meal.objects.filter(name__contains=search_text[search_text_i]))
        search_result_list_len[search_text_i] = 0
        # 26-29行：先获取单字搜索【结果数量最多】的字的下标，再对该下标对应的原字符串中的字进行filter，而后将该下标对应的搜索结果数量置0，标记为已搜索
        while i < search_text_len:
            search_result_list_max = max(search_result_list_len)
            if search_result_list_max == 0:
                break
            # 该if语句为避免重复对已置0，即标记为已搜索字再次搜索
            search_text_i = search_result_list_len.index(search_result_list_max)
            if len(search_result_list_final[i - 1].filter(name__contains=search_text[search_text_i])) == 0:
                break
            # 该if语句为当链式搜索中途无搜索结果时结束循环
            search_result_list_final.append(
                search_result_list_final[i - 1].filter(name__contains=search_text[search_text_i]))
            i = i + 1
        search__result = search_result_list_final[i - 1]  # 获取链式搜索最终结果
        content = {'search__result': search__result}

        return render(request, 'meals/search_result.html', content)
    else:
        return render(request, 'meals/index.html')


# 问题详情 & 发表评论  李积栋5.4接受前端的字符串，删除了表单
def detail(request, meal_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')

    meal = Meal.objects.get(id=meal_id)
    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    if request.method == 'POST':  # post请求提交评论
        comment_content = request.POST.get('message')  # 获取前端输入内容
        if comment_content:
            Comment.objects.create(user=user, meal=meal, content=comment_content)
    # 创建评论
    if request.method == 'GET':  # get请求让浏览量加一
        meal.views += 1
        meal.save()
    comments = Comment.objects.filter(meal=meal)
    tags = Tag.objects.filter(meal=meal)
    current_user_like_comment_list = []  # 此列表将保存当前用户对当前菜品的评论中点过赞的评论的id
    for com in comments:
        current_comment = LikeComment.objects.filter(comment=com)
        for cc in current_comment:
            if cc.user == user:
                current_user_like_comment_list.append(com.id)
    """
    通过三个bool变量like,dislike,collect分别表示用户是否对菜品点过赞，是否踩过菜品，是否收藏过菜品。
    
    通过current_user_like_comment_list中的comment的id值，前端可确定当前用户是否对某条评论点过赞，从而确定显示底色
    """
    if LikeMeal.objects.filter(user=user, meal=meal):
        like = True
    else:
        like = False

    if DislikeMeal.objects.filter(user=user, meal=meal):
        dislike = True
    else:
        dislike = False

    if CollectMeal.objects.filter(user=user, meal=meal):
        collect = True
    else:
        collect = False

    content = {'meal': meal, 'comments': comments, 'tags': tags, 'like': like, 'dislike': dislike,
               'collect': collect, 'current_user_like_comment_list': current_user_like_comment_list}
    return render(request, 'meals/detail.html', content)


# 处理点赞，点踩和收藏的函数 5.5李积栋
def like_meal(request, meal_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')

    if request.method == 'GET':
        user = User.objects.get(id=request.session['user_id'])
        meal = Meal.objects.get(id=meal_id)
        like_record = LikeMeal.objects.filter(user=user, meal=meal)
        if like_record:
            like_record = LikeMeal.objects.get(user=user, meal=meal)
            like_record.delete()
            meal.likes -= 1
            meal.save()
        else:
            LikeMeal.objects.create(user=user, meal=meal)
            meal.likes += 1
            meal.save()
            if DislikeMeal.objects.filter(user=user, meal=meal):
                dislike_record = DislikeMeal.objects.get(user=user, meal=meal)
                dislike_record.delete()
                meal.dislikes -= 1
                meal.save()
    return redirect('meals:detail', meal_id=meal_id)


def dislike_meal(request, meal_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')

    if request.method == 'GET':
        user = User.objects.get(id=request.session['user_id'])
        meal = Meal.objects.get(id=meal_id)
        dislike_record = DislikeMeal.objects.filter(user=user, meal=meal)
        if dislike_record:
            dislike_record = DislikeMeal.objects.get(user=user, meal=meal)
            dislike_record.delete()
            meal.dislikes -= 1
            meal.save()
        else:
            DislikeMeal.objects.create(user=user, meal=meal)
            meal.dislikes += 1
            meal.save()
            if LikeMeal.objects.filter(user=user, meal=meal):
                like_record = LikeMeal.objects.get(user=user, meal=meal)
                like_record.delete()
                meal.likes -= 1
                meal.save()
    return redirect('meals:detail', meal_id=meal_id)


def like_comment(request, comment_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')

    user = User.objects.get(id=request.session['user_id'])
    comment = Comment.objects.get(id=comment_id)
    meal_id = comment.meal.id
    if request.method == 'GET':
        like_record = LikeComment.objects.filter(user=user, comment=comment)
        if like_record:
            like_record = LikeComment.objects.get(user=user, comment=comment)
            like_record.delete()
            comment.likes -= 1
            comment.save()
        else:
            LikeComment.objects.create(user=user, comment=comment)
            comment.likes += 1
            comment.save()
    return redirect('meals:detail', meal_id=meal_id)


def collect_meal(request, meal_id):
    if not request.session.get('is_login', None):  # 如果未登录，跳转到登录页面
        return redirect('/meals/login/')

    if request.method == 'GET':
        user = User.objects.get(id=request.session['user_id'])
        meal = Meal.objects.get(id=meal_id)
        collect_record = CollectMeal.objects.filter(user=user, meal=meal)
        if collect_record:
            collect_record = CollectMeal.objects.get(user=user, meal=meal)
            collect_record.delete()
        else:
            CollectMeal.objects.create(user=user, meal=meal)
    return redirect('meals:detail', meal_id=meal_id)


# 登录页面，已完成
def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/meals/index/')
    if request.method == 'POST':
        login_form = UserLoginForm(request.POST)
        message = '亲，好像内容不太对哦~'
        if login_form.is_valid():
            username = login_form.cleaned_data.get('user_name')
            password = login_form.cleaned_data.get('password')
            try:
                user = User.objects.get(user_name=username)
            except:
                message = '亲，小生没有查到您的账户哦(⊙o⊙)'
                return render(request, 'meals/login.html', locals())
            string = password + user.salt
            hl = hashlib.md5()
            hl.update(string.encode(encoding='utf-8'))
            password = hl.hexdigest()
            if user.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name
                return redirect('/meals/index/')
            else:
                message = '亲，密码好像不对哦~'
                return render(request, 'meals/login.html', locals())
        else:
            return render(request, 'meals/login.html', locals())
    login_form = UserLoginForm()

    return render(request, 'meals/login.html', locals())


def generate_random_str(random_length=4):
    """
  生成一个指定长度的随机字符串
  """
    random_str = ''
    base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
    length = len(base_str) - 1
    for i in range(random_length):
        random_str += base_str[random.randint(0, length)]
    return random_str


# 账户注册页面,已完成
def register(request):
    if request.session.get('is_login', None):
        return redirect('/meals/index/')

    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            user_name = register_form.cleaned_data.get('user_name')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')

            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'meals/register.html', locals())
            else:
                same_name_user = User.objects.filter(user_name=user_name)
                if same_name_user:
                    message = '该用户名已经存在'
                    return render(request, 'meals/register.html', locals())
                salt = generate_random_str(random_length=4)
                password = password1 + salt
                hl = hashlib.md5()
                hl.update(password.encode(encoding='utf-8'))
                User.objects.create(user_name=user_name, salt=salt, password=hl.hexdigest())
                return redirect('/meals/login/')
        else:
            return render(request, 'meals/register.html', locals())
    register_form = RegisterForm()
    return render(request, 'meals/register.html', locals())


# 退出登录，已完成
def logout(request):
    if not request.session.get('is_login', None):  # 如果本来就未登录，也就没有登出一说
        return redirect("/meals/login/")
    request.session.flush()
    return redirect("/meals/login/")


# 菜单和菜单内部标签筛选函数
# 5.3 黄祖华 更改为多标签筛选
def menu(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meals/login/')

    # 通过用户选择的标签确定下一步删选结果函数的参数
    try:
        tags = request.POST['Tag']
        # 每点一个tag均添加至列表selected_tags中保存
    except KeyError:
        # 如果用户没有筛选标签，则重新返回菜单页面
        all_meals = Meal.objects.all()
        return render(request, 'meals/menu.html', {'all_meals': all_meals})
    if len(tags) != 0:
        tags_dict = {'1': '麻辣可口', '2': '清爽', '3': '荤菜', '4': '素菜', '5': '低卡', '6': '高卡'}
        tags_result_list = []
        # tags_result_list为用以迭代查询的列表，实现与关系查询
        i = 0
        tags_result_list.append(Meal.objects.filter(tag__tag__contains=tags_dict[tags[0]]))
        for x in tags:
            i = i + 1
            tags_result_list.append(tags_result_list[i - 1].filter(tag__tag__contains=tags_dict[x]))
        tags_search_result = tags_result_list[i]
    else:
        # 如果tags为空
        all_meals = Meal.objects.all()
        return render(request, 'meals/menu.html', {'all_meals': all_meals})
    return render(request, 'meals/menu.html', {'all_meals': tags_search_result})


# 李积栋 5.1 新增用户个人主页及用户修改
# 个人信息
def myself(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meals/login/')

    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    collected_meals = CollectMeal.objects.filter(user=user)  # 某用户收藏的所有菜品集合
    content = {'user': user, 'collect_meal': collected_meals}
    return render(request, 'meals/myself.html', content)


def myself_mealcollect(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meals/login/')

    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    collected_meals = CollectMeal.objects.filter(user=user)  # 某用户收藏的所有菜品集合
    content = {'user': user, 'collect_meal': collected_meals}
    return render(request, 'meals/myself_mealcollect.html', content)


def myself_meallike(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meals/login/')

    user = User.objects.get(id=request.session['user_id'])  # 从会话获取用户id
    liked_meals = LikeMeal.objects.filter(user=user)  # 某用户收藏的所有菜品集合
    content = {'user': user, 'like_meal': liked_meals}
    return render(request, 'meals/myself_meallike.html', content)


# 修改个人信息
def modify_myself(request):
    if not request.session.get('is_login', None):  # 如果未登录， 跳转到登录页面
        return redirect('/meals/login/')
    print(request.POST)
    user = User.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        modify_myself_form = ModifyMyselfForm(request.POST, request.FILES)
        message = '请检查填写的内容'
        if modify_myself_form.is_valid():
            # 检查是否新用户名是否已被使用
            user_name = modify_myself_form.cleaned_data.get('user_name')
            some_user1 = User.objects.filter(user_name=user_name).filter(id__lt=user.id)  # 查找id和此用户不同，是否有重名
            some_user2 = User.objects.filter(user_name=user_name).filter(id__gt=user.id)
            message = '这个用户名已经有人使用了哦'
            content = {'message': message, 'user': user}
            if some_user1 or some_user2:
                return render(request, 'meals/modify_myself.html', content)  # 返回表单和提示信息让用户重新填写
            # 修改数据库中的信息
            user.user_name = user_name
            password = modify_myself_form.cleaned_data.get('password')
            salt = user.salt
            password = password + salt
            hl = hashlib.md5()
            hl.update(password.encode(encoding='utf-8'))
            user.password = hl.hexdigest()
            user.telephone = modify_myself_form.cleaned_data.get('telephone')
            user.email = modify_myself_form.cleaned_data.get('email')
            if 'avatar' in request.FILES:
                user.avatar = modify_myself_form.cleaned_data.get('avatar')  # 判断用户是否上传了图片
            user.save()
            message = '修改成功'
            content = {'message': message, 'user': user}
            return render(request, 'meals/modify_myself.html', content)  # 修改了用户信息并返回提示信息
        content = {'message': message, 'user': user}
        return render(request, 'meals/modify_myself.html', content)
    modify_myself_form = ModifyMyselfForm()
    content = {'modify_myself_form': modify_myself_form, 'user': user}
    return render(request, 'meals/modify_myself.html', content)  # 返回空表单让用户填写
