from django.urls import path

from . import views

app_name = 'meals'  # 使用名字空间

urlpatterns = [

    # 首页
    path('index/', views.index, name='index'),

    # 菜品详情
    path('detail/<int:meal_id>/', views.detail, name='detail'),

    # 登录页面
    path('login/', views.login, name='login'),

    # 注册页面
    path('register/', views.register, name='register'),

    # 退出登录
    path('logout/', views.logout, name='logout'),

    # 菜单和菜单内标签筛选 ,启动筛选功能
    path('menu/', views.menu, name='menu'),

    # 用户个人主页
    path('myself/', views.myself, name='myself'),
    path('myself_mealcollect/', views.myself_mealcollect , name='myself_mealcollect'),
    path('myself_meallike/', views.myself_meallike, name='myself_meallike'),
    # 更改个人信息
    path('modify_myself/', views.modify_myself, name='modify_myself'),

    # 处理用户点赞，点踩,收藏
    path('like_meal/<int:meal_id>/', views.like_meal, name='like_meal'),
    path('dislike_meal/<int:meal_id>/', views.dislike_meal, name='dislike_meal'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('collect_meal/<int:meal_id>/', views.collect_meal, name='collect_meal'),
    path('search_result/', views.search_result, name='search_result'),
]
