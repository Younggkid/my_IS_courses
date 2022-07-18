from django import forms
from meals.models import Comment, User


# 用户登录表单
class UserLoginForm(forms.Form):
    user_name = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': "Password"}))


# 注册账户表单
class RegisterForm(forms.Form):
    user_name = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password1 = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="确认密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    # email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # telephone = forms.CharField(label="电话号码", max_length=128, widget=forms.TextInput(
        # attrs={'class': 'form-control'}))


# 用户搜索表单
class SearchForm(forms.Form):
    search_text = forms.CharField(label="搜索", max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请输入搜索内容'}
    ))


# 用户评论表单
class CommentForm(forms.Form):
    class Meta:
        model = Comment
        fields = ['content']


# 修改个人信息表单
class ModifyMyselfForm(forms.Form):
    avatar = forms.ImageField()
    user_name = forms.CharField(label="用户名", max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': "Username", 'autofocus': ''}))
    password = forms.CharField(label="密码", max_length=256, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(label="邮箱地址", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    telephone = forms.CharField(label="电话号码", max_length=128, widget=forms.TextInput(
                attrs={'class': 'form-control'}))
