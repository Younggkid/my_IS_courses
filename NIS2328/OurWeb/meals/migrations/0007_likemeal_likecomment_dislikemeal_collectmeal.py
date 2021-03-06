# Generated by Django 4.0.3 on 2022-05-04 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meals', '0006_alter_tag_options_alter_meal_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='LikeMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.user')),
            ],
        ),
        migrations.CreateModel(
            name='LikeComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.user')),
            ],
        ),
        migrations.CreateModel(
            name='DislikeMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.user')),
            ],
        ),
        migrations.CreateModel(
            name='CollectMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.meal')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='meals.user')),
            ],
        ),
    ]
