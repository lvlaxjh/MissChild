'''
Author: your name
Date: 2020-08-18 13:51:41
LastEditTime: 2020-09-28 23:52:35
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /steamsearch/mainapp/admin.py
'''
from django.contrib import admin
from mainapp.models import *

admin.site.register(People)
admin.site.register(PeopleImg)
admin.site.register(Statistics)
admin.site.register(User)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(newsImg)
