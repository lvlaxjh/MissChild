'''
Author: your name
Date: 2020-08-18 13:51:41
LastEditTime: 2020-09-29 08:59:50
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
admin.site.register(Statistics2)
