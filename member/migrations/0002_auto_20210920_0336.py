# Generated by Django 3.2.6 on 2021-09-19 18:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='exercise_frequency',
            field=models.CharField(choices=[('VO', '매우 자주'), ('U', '자주'), ('S', '가끔'), ('H', '거의 안함'), ('N', '안함')], max_length=2, verbose_name='운동 빈도'),
        ),
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(regex='/^(?=.*\\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{5,16}$/')], verbose_name='사용자 비밀번호'),
        ),
        migrations.AlterField(
            model_name='user',
            name='useremail',
            field=models.EmailField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator(regex='[\\w\\.-]+@[\\w\\.-]+')], verbose_name='사용자 이메일'),
        ),
        migrations.AlterField(
            model_name='user',
            name='userid',
            field=models.CharField(max_length=64, unique=True, validators=[django.core.validators.RegexValidator(regex='/^[a-z]+[a-z0-9]{2,9}$/g')], verbose_name='사용자 아이디'),
        ),
    ]
