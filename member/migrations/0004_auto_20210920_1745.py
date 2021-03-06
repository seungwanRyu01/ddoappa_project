# Generated by Django 3.2.6 on 2021-09-20 08:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20210920_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=64, validators=[django.core.validators.RegexValidator(message='only valid email is required', regex='/^(?=.*\\d)(?=.*[a-zA-Z])[0-9a-zA-Z]{5,16}$/')], verbose_name='사용자 비밀번호'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phoneNumber',
            field=models.CharField(max_length=16, unique=True, validators=[django.core.validators.RegexValidator(message='only valid email is required', regex='^\\+?1?\\d{8,15}$')], verbose_name='사용자 전화번호'),
        ),
        migrations.AlterField(
            model_name='user',
            name='useremail',
            field=models.EmailField(max_length=32, unique=True, validators=[django.core.validators.RegexValidator(message='only valid email is required', regex='[\\w\\.-]+@[\\w\\.-]+')], verbose_name='사용자 이메일'),
        ),
        migrations.AlterField(
            model_name='user',
            name='userid',
            field=models.CharField(max_length=64, unique=True, validators=[django.core.validators.RegexValidator(message='only valid email is required', regex='/^[a-z]+[a-z0-9]{2,9}$/g')], verbose_name='사용자 아이디'),
        ),
    ]
