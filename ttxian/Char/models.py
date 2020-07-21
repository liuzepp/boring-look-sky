from django.db import models

# Create your models here.
class CartInfo(models.Model):
    user=models.ForeignKey('Login.User')
    goods=models.ForeignKey('Goodshow.GoodsInfo')
    count=models.IntegerField()
