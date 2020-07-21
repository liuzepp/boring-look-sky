# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('uname', models.CharField(max_length=20)),
                ('upwd', models.CharField(max_length=40)),
                ('uemail', models.CharField(max_length=30)),
                ('isValid', models.BooleanField(default=True)),
                ('isActive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserAddressInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('uname', models.CharField(max_length=20)),
                ('uaddress', models.CharField(max_length=100)),
                ('uphone', models.CharField(max_length=11)),
                ('user', models.ForeignKey(to='Login.User')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nickname', models.CharField(verbose_name='昵称', max_length=30, blank=True, null=True)),
                ('birthday', models.DateField(verbose_name='生日', blank=True, null=True)),
                ('sex', models.CharField(verbose_name='性别', max_length=10, default='man', choices=[('woman', '女'), ('man', '男')])),
                ('profile_photo', models.ImageField(verbose_name='用户头像', default='profile_photo/default.png', upload_to='profile_photo/%Y/%m')),
                ('isValid', models.BooleanField(default=True)),
                ('isActive', models.BooleanField(default=False)),
                ('user', models.ForeignKey(to='Login.User')),
            ],
        ),
    ]
