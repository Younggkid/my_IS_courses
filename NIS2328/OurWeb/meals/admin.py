from django.contrib import admin
from meals import models
# 注册了已存在的数据库中的模型

admin.site.register(models.User)
admin.site.register(models.Meal)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.LikeMeal)
admin.site.register(models.DislikeMeal)
admin.site.register(models.CollectMeal)
admin.site.register(models.LikeComment)
