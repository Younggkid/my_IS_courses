from django.db import models


# 李积栋4.15
# 用户类
class User(models.Model):
    user_name = models.CharField(max_length=20, unique=True, verbose_name='用户名', blank=False, null=False)
    salt = models.CharField(max_length=4, verbose_name='密钥')
    password = models.CharField(max_length=200, verbose_name='密码', null=False, blank=False)
    avatar = models.ImageField(upload_to='user_avatar/', verbose_name='头像', blank=True, null=True,
                               default='user_avatar/default0.jpg')
    telephone = models.CharField(max_length=11, null=True, verbose_name='电话号', blank=True)
    email = models.EmailField(blank=True, null=True, verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.user_name

    class Meta:
        ordering = ['-create_time']  # 按时间递减排序
        verbose_name = "用户"
        verbose_name_plural = "用户"


# 这是菜品类
class Meal(models.Model):
    name = models.CharField(max_length=30)  # 菜名
    picture = models.ImageField(upload_to='meal_picture/', default='default_meal_picture.jpg')  # 图片
    price = models.FloatField(default=0.0)  # 价格
    canteen = models.CharField(max_length=20)  # 所在餐厅，如，第一餐饮大楼
    place = models.CharField(max_length=60)  # 具体位置，如，二楼东侧木桶饭
    likes = models.IntegerField(default=0, verbose_name='点赞数')  # 点赞数，默认为零
    dislikes = models.IntegerField(default=0, verbose_name='差评数')  # 差评数，默认为零
    views = models.IntegerField(default=0, verbose_name='浏览量')

    def __str__(self):  # 返回对象时显示字符串
        return self.name

    class Meta:
        ordering = ['-likes']  # 按点赞数递减排序
        verbose_name = "菜品"
        verbose_name_plural = "菜品"


# 这是评论类
class Comment(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)  # 每一条评论所归属的菜名
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=2000)  # 评论内容
    pub_date = models.DateField(auto_now_add=True)  # 发布日期,自动保存评论的创建日期
    pub_time = models.TimeField(auto_now_add=True)  # 发布时间，自动保存评论的创建时间
    likes = models.IntegerField(default=0)  # 评论点赞数

    def __str__(self):
        return '%s Comment:%s' % (self.meal.name, self.content)

    class Meta:
        ordering = ['-pub_date', '-pub_time']  # 按时间递减排序
        verbose_name = "评论"
        verbose_name_plural = "评论"


# 这是菜品的标签类
class Tag(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)  # 所属菜品
    tag = models.CharField(max_length=12)  # 标签

    def __str__(self):
        return '%s\'s Tag:%s' % (self.meal.name, self.tag)

    class Meta:
        verbose_name_plural = "标签"


# 这是对于菜品的点赞类
class LikeMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return '%s赞了%s' % (self.user.user_name, self.meal.name)


# 这是对于菜品的点踩类
class DislikeMeal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    def __str__(self):
        return '%s踩了%s' % (self.user.user_name, self.meal.name)


# 这是对于某条评论的点赞类
class LikeComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    def __str__(self):
        return '%s赞了评论%d' % (self.user.user_name, self.comment.id)


# 这是用户收藏某菜品类
class CollectMeal(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s收藏了%s' % (self.user.user_name, self.meal.name)