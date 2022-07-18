from django.test import TestCase, Client
from django.urls import resolve, reverse
from .views import *
from .models import *
from .forms import *
from django.db.utils import IntegrityError as Integrity1Error


class TestModel(TestCase):  # 这部分是对models中的模型实例进行测试，包含测试创建评论，测试用户名不能重名等。

    def test_comment(self):  # 测试评论创建是否可行
        example = Comment(meal=Meal(id=1), user=User(id=1), content='very good')
        self.assertEqual(example.meal.id, 1)
        self.assertEqual(example.user.id, 1)
        self.assertEqual(example.content, 'very good')
        self.assertEqual(example.likes, 0)  # 测试评论点赞数的默认值是否为0

    def test_user_unique(self):  # 测试user_name的unique=True
        u1 = User(user_name='a')
        u1.save()  # 先保存一个用户名为a的用户
        with self.assertRaises(Integrity1Error):
            User.objects.create(user_name='a')  # 此时若再创建一个用户名为a的用户， 则会引发数据库的IntegrityError,
            # 表示产生了预期的错误，即用户名不能重名

    def test_meal(self):  # 测试新建一个菜品时点赞数、点踩数浏览量、价格是否为零
        a = Meal()
        self.assertEqual(a.likes, 0)
        self.assertEqual(a.dislikes, 0)
        self.assertEqual(a.views, 0)
        self.assertEqual(a.price, 0.0)

    def test_like_meal(self):  # 测试菜品点赞的创建
        test_like_meal = LikeMeal(user=User(id=1), meal=Meal(id=1))
        self.assertEqual(test_like_meal.meal, Meal(id=1))
        self.assertEqual(test_like_meal.user, User(id=1))

    def test_dislike_meal(self):  # 测试菜品点踩的创建
        a = DislikeMeal(user=User(id=1), meal=Meal(id=1))
        self.assertEqual(a.user, User(id=1))
        self.assertEqual(a.meal, Meal(id=1))

    def test_like_comment(self):  # 测试评论点赞的创建
        b = LikeComment(user=User(id=1), comment=Comment(id=1))
        self.assertEqual(b.user, User(id=1))
        self.assertEqual(b.comment, Comment(id=1))

    def test_collect_meal(self):  # 测试用户收藏菜品的创建
        c = CollectMeal(user=User(id=1), meal=Meal(id=1))
        self.assertEqual(c.user, User(id=1))
        self.assertEqual(c.meal, Meal(id=1))


class TestLoginLogoutRegister(TestCase):  # 测试登录注册相关的功能， 主要是测试服务器是否处理了用户请求，是否返回了正确的html文件
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('meals:login')  # 先通过reverse获取url路径
        self.register_url = reverse('meals:register')
        self.logout_url = reverse('meals:logout')

    def test_register(self):
        user1 = {'user_name': 'user1', 'password': '123', 'telephone': '123456',
                 'email': 'user1@qq.com'}
        response = self.client.post(self.register_url, data=user1)
        self.assertEqual(response.status_code, 200)  # 状态码为200表示服务器成功处理了注册请求
        self.assertTemplateUsed(response, 'meals/register.html')  # 检测使用的模板是否为register.html

    def test_login(self):
        user2 = {'user_name': 'user2', 'password': '123', 'telephone': '1234556',
                 'email': 'user2@qq.com'}
        response = self.client.post(self.login_url, data=user2)
        self.assertEqual(response.status_code, 200)  # 状态码为200表示服务器成功处理了注册请求
        self.assertTemplateUsed(response, 'meals/login.html')  # 使用的template是否为login.html

    def test_logout(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)  # 302表示请求的网页暂时跳转到其他页面， 也就是logout跳转到login页面

    def tearDown(self):
        pass


class TestViews(TestCase):  # 测试视图函数中其他函数的功能
    def setUp(self):
        Meal.objects.create(id=1)
        User.objects.create(id=2)
        Comment.objects.create(id=3, meal=Meal(id=1), user=User(id=2))
        User.objects.create(user_name='test', password='test')
        self.client = Client()
        self.client.post('/meals/login/', {'user_name': 'test', 'password': 'test'})  # 使用post发送请求，登录一个实例用户以便测试

    def test_like_meal(self):  # 测试处理点赞的函数
        response = self.client.get('/meals/like_meal/1/')  # 对id=1的meal进行点赞操作
        self.assertEqual(response.status_code, 302)  # 302表示请求的网页暂时跳转到其他页面， 即重定向到detail页面

    def test_dislike_meal(self):  # 测试处理点踩的函数
        response = self.client.get('/meals/dislike_meal/1/')
        self.assertEqual(response.status_code, 302)

    def test_like_comment(self):  # 测试处理评论点赞的函数

        response = self.client.get('/meals/like_comment/3/')
        self.assertEqual(response.status_code, 302)

    def test_myself_mealcollect(self):  # 测试用于显示用户收藏的菜品的函数
        response = self.client.get('/meals/myself_mealcollect/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meals/myself_mealcollect.html')

    def test_myself_meallike(self):   # 测试用于显示用户点赞的菜品的函数
        response = self.client.get('/meals/myself_meallike/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'meals/myself_meallike.html')

    def test_myself(self):  # 测试用户主页函数

        response = self.client.get('/meals/myself/')
        self.assertTemplateUsed(response, 'meals/myself.html')  # 测试使用的是否为对应的html文件
        self.assertEqual(response.status_code, 200)  # 200表示服务器成功处理了请求

    def test_menu(self):  # 测试菜单中的标签筛选功能

        response = self.client.post('/meals/menu/', {'Tag': 1})  # 使用value值为1的标签进行筛选
        self.assertEqual(response.status_code, 200)  # 200表示服务器正确处理了post请求
        self.assertTemplateUsed(response, 'meals/menu.html')

    def test_search(self):  # 测试首页的搜索功能
        response = self.client.post('/meals/search_result/', {'search_data': '辣'})  # 用户输入设置为‘辣’
        self.assertTemplateUsed(response, 'meals/search_result.html')  # 是否使用了对应的html文件
        self.assertEqual(response.status_code, 200)  # 200表示服务器正确处理了post请求

    def test_modify(self):
        response = self.client.post('/meals/modify_myself/', {})  # 测试修改个人信息功能
        self.assertEqual(response.status_code, 200)  # 200表示服务器正确处理了post请求
        self.assertTemplateUsed(response, 'meals/modify_myself.html')

    def tearDown(self):
        pass
