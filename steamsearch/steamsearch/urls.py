'''
Author: your name
Date: 2020-08-18 13:51:13
LastEditTime: 2020-09-27 15:53:09
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /steamsearch/steamsearch/urls.py
'''
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static
from django.views import static
from django.conf import settings
urlpatterns = [
    url('^$', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('res/<searchContent>/',
        views.searchResults, name='results'),
    path('content/<ID>/',
         views.oneContent, name='content'),
    # path('manager/check/',views.check, name='check'),
    # path('manager/', views.managerLogin, name='manager'),
    path('apidoc',views.apidoc,name='apidoc'),
    path('api/<content>/', views.useApi,name='api'),
    # # path('api/databaseBasicInformation/', views.databaseBasicInformation,
    # #      name='databaseBasicInformation'),
    # url(r'^static/(?P<path>.*)$', static.serve,
    #     {'document_root': settings.STATIC_ROOT}, name='media'),
   	url(r'^media/(?P<path>.*)$', static.serve,
   	    {'document_root': settings.MEDIA_ROOT}, name='media')
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
