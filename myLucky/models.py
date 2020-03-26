from django.db import models

# Create your models here.

from django.db import models


class Prize(models.Model):
    name = models.CharField(max_length=50)
    name.verbose_name = '奖品名'
    ptype = models.CharField(max_length=2)
    num = models.IntegerField()
    joinNum = models.IntegerField(default=0)
    content = models.CharField(max_length=150)
    url = models.CharField(max_length=100, null=True, blank=True)
    img = models.CharField(max_length=100, default="media/img/default.png")
    creatTime = models.DateTimeField(auto_now_add=True)
    usedTime = models.DateTimeField(null=True)
    code = models.CharField(max_length=10, null=True, blank=True)
    isUsed = models.BooleanField(default=False)
    puser = models.ForeignKey("User", on_delete=models.CASCADE)

    class Meta:
        db_table = "prize"
        ordering = ['id']



class User(models.Model):
    account = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=11)
    pwd = models.CharField(max_length=50)
    img = models.CharField(max_length=100, default="media/img/default.png")
    creatTime = models.DateTimeField(auto_now_add=True)
    userToken = models.CharField(max_length=50)
    sign = models.BooleanField(default=False)
    isDelete = models.BooleanField(default=False)

    class Meta:
        db_table = "user"
        ordering = ['id']



class Attach(models.Model):
    attachTime = models.DateTimeField(auto_now_add=True)
    isLucky = models.BooleanField(null=True, blank=True)
    attachUser = models.ForeignKey("User", on_delete=models.CASCADE)
    attachPrize = models.ForeignKey("Prize", on_delete=models.CASCADE)

    class Meta:
        db_table = "attach"
        ordering = ["id"]
