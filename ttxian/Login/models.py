from django.db import models

# Create your models here.
class User(models.Model):
    uname=models.CharField(max_length=20)
    upwd=models.CharField(max_length=40)
    uemail=models.CharField(max_length=30)
    isValid=models.BooleanField(default=True)
    isActive=models.BooleanField(default=False)

    def __str__(self):
        return self.uname
class UserAddressInfo(models.Model):
    uname=models.CharField(max_length=20)
    uaddress=models.CharField(max_length=100)
    uphone=models.CharField(max_length=11)
    user=models.ForeignKey('User')

    def __str__(self):
        return self.uname

class UserInfo(models.Model):
    nickname = models.CharField(max_length=30, verbose_name=u'昵称', null=True, blank=True)
    birthday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    sex = models.CharField(
        max_length=10, choices=(('woman', '女'), ('man', u'男')),
        default='man', verbose_name=u'性别'
    )
    profile_photo = models.ImageField(
        upload_to='profile_photo/%Y/%m',
        verbose_name=u'用户头像',
        default='profile_photo/default.png',
        max_length=100
    )
    isValid=models.BooleanField(default=True)
    isActive=models.BooleanField(default=False)
    user = models.ForeignKey('User')