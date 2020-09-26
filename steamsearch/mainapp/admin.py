'''
Author: your name
Date: 2020-08-18 13:51:41
LastEditTime: 2020-09-26 21:07:37
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /steamsearch/mainapp/admin.py
'''
from django.contrib import admin
from mainapp.models import *

admin.site.register(People)
admin.site.register(PeopleImg)
admin.site.register(Statistics)
admin.site.register(Manage)
