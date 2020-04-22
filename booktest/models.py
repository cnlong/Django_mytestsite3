from django.db import models

# Create your models here.
# 直接新建类，不用迁移，就可以调用数据库内容
class BookInfo(models.Model):
    """图书信息类"""
    btitle = models.CharField(max_length=20)
    bpub_date = models.DateField()
    bread = models.IntegerField(default=0)
    bcomment = models.IntegerField(default=0)
    isDelete = models.BooleanField(default=False)
