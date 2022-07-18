# Generated by Django 4.0.3 on 2022-04-14 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('picture', models.ImageField(default=None, upload_to='images')),
                ('price', models.FloatField(default=0.0)),
                ('canteen', models.CharField(max_length=20)),
                ('place', models.CharField(max_length=60)),
                ('likes', models.IntegerField(default=0, verbose_name='点赞数')),
                ('dislikes', models.IntegerField(default=0, verbose_name='差评数')),
                ('views', models.IntegerField(default=0, verbose_name='浏览量')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=200, verbose_name='密码')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='user_avatar/', verbose_name='头像')),
                ('telephone', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话号')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='邮箱')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'ordering': ['-create_time'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=12)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=2000)),
                ('pub_date', models.DateField(auto_now=True)),
                ('pub_time', models.TimeField(auto_now=True)),
                ('likes', models.IntegerField(default=0)),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.user')),
            ],
        ),
    ]