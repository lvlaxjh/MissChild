'''
Author: your name
Date: 2020-08-18 13:51:41
LastEditTime: 2020-09-26 21:06:51
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /steamsearch/mainapp/models.py
'''
from django.db import models


# 失联者信息
class People(models.Model):
    id = models.AutoField("唯一id", primary_key=True)
    name = models.TextField("走失者-姓名", default="none")
    sex = models.TextField("走失者-性别", default="0")#0:男，1:女，2:其他
    birthday = models.TextField("走失者-出生日期", default="none$none$none")#格式为：年-月-日
    height = models.TextField(
        "走失者-身高", default="none")
    weight = models.TextField(
        "走失者-体重", default="none")
    timeL = models.TextField(
        "走失者-出生日期", default="none$none$none$none$none")  # 格式为：年-月-日-时-分
    site = models.TextField("走失者-走失地区", default="none")
    text = models.TextField("走失者-描述", default="none")
    kinName = models.TextField("亲属-称呼", default="none")
    kinLink = models.TextField("亲属-联系方式", default="none")


#失联者图片
class PeopleImg(models.Model):
    id = models.AutoField("唯一id", primary_key=True)
    onePeople = models.ForeignKey(
        People, on_delete=models.CASCADE, verbose_name="该图片所属信息", default=1)
    imgFile = models.ImageField(
        "失联者图片", upload_to="checkImg", null=True, blank=True)
#网站记录
class Statistics(models.Model):
    id = models.AutoField("唯一id", primary_key=True)
    visits = models.IntegerField("访问次数", default=0)
    search = models.IntegerField("搜索次数", default=0)
    # allrecord = models.IntegerField("登记数量", default=0)
    upload = models.IntegerField("上传次数", default=0)
#管理员账号
class Manage(models.Model):
    id = models.AutoField("唯一id", primary_key=True)
    user = models.TextField("账号", default="none")
    password = models.TextField("密码", default="none")