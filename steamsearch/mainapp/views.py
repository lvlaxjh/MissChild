from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mainapp.models import *
import re
import time
import sys

'''
----------------------------------------------------------------------------------------------------------------------------------------------
功能函数
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def errorFunc(request, e, erLine):
    print("********************************500-Error-start********************************")
    print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print("errorContent:    "+str(e))
    print("errorLine:   "+str(erLine))
    print("********************************500-Error-end********************************")
    return render(request, '500.html', {"error": e, "erLine": erLine})


'''
----------------------------------------------------------------------------------------------------------------------------------------------
主界面
----------------------------------------------------------------------------------------------------------------------------------------------
'''

def index(request):
    content = {
        'visits': 0,
        'search': 0,
        'allrecord': 0,
        'upload': 0,
    }
    try:
        # 站内统计-start
        content['allrecord'] = People.objects.all().count()
        stat = Statistics.objects.get(id=1)
        content['visits'] = stat.visits
        content['search'] = stat.search
        content['upload'] = stat.upload
        stat.visits += 1
        stat.save()
        # 站内统计-end
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)
    if request.method == 'POST':
        try:
            searchButton = request.POST.get('searchButton')
            subButton = request.POST.get('subInf')
        except Exception as e:
            return errorFunc(request, e, sys._getframe().f_lineno)
        if searchButton == 'searchButton':
            try:
                # 站内统计-start
                stat = Statistics.objects.get(id=1)
                stat.search += 1
                stat.save()
                # 站内统计-end
            except Exception as e:
                return errorFunc(request, e, sys._getframe().f_lineno)
            try:
                # 搜索-start
                searchContent = request.POST.get('searchContent')
                searchSelect = request.POST.get('searchSelect')
                if searchContent == '':  # 搜索为空刷新主页
                    return redirect('index')
                else:  # url反转搜索内容
                    pass
                    # return redirect(reverse('results', kwargs={'searchContent': str(searchContent), 'searchSelect': str(searchSelect), 'u': '*', 'p': '*'}))
                # 搜索-end
            except Exception as e:
                return errorFunc(request, e, sys._getframe().f_lineno)
        # 上传信息-start
        if subButton == 'subInf':
            try:
                # 站内统计-start
                stat = Statistics.objects.get(id=1)
                stat.upload += 1
                stat.save()
                # 站内统计-end
            except Exception as e:
                return errorFunc(request, e, sys._getframe().f_lineno)
            try:
                theUrl = request.POST.get('committerUrl')
                # 处理上传url-start
                '''
                    正则判断格式是否为合法url，若不合法补充为http://形式
                '''
                if len(theUrl) > 0:
                    urlpattern = re.compile(
                        r'^(?:http|ftp)s?://'  # http:// or https://
                        # domain...
                        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                        r'localhost|'  # localhost...
                        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                        r'(?::\d+)?'  # optional port
                        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
                    if urlpattern.match(theUrl) == None:
                        theUrl = 'http://' + theUrl
                # 处理上传url-end
                else:
                    theUrl = "none"
                requestDic = {
                    "committerInformation": request.POST.get('committerInformation'),
                    "committerUrl": theUrl,
                    #
                    "reportQq": request.POST.get('reportQq'),
                    "reportVx": request.POST.get('reportVx'),
                    "reportSteam": request.POST.get('reportSteam'),
                    "reportAliPay": request.POST.get('reportAliPay'),
                    "reportMaxId": request.POST.get('reportMaxId'),
                    "reportHeiBox": request.POST.get('reportHeiBox'),
                    "reportTieBa": request.POST.get('reportTieBa'),
                }
                oneInf = ToExamine.objects.create(**requestDic)  # 数据库增加一条数据
                for i in request.FILES.getlist("imgFile"):
                    checkImg = ExamineImg.objects.create(
                        examine=oneInf, imgFile=i)  # 存储上传图片
                    checkImg.save()
                oneInf.save()
                for key, value in requestDic.items():
                    if value == '':
                        requestDic[key] = 'none'
                return redirect('index')  # 上传完成后刷新页面（防止了刷新页面重复提交表单）
            except Exception as e:
                return errorFunc(request, e, sys._getframe().f_lineno)
        # 上传信息end--------------------------------------------------------------
    return render(request, 'index.html', content)


'''
----------------------------------------------------------------------------------------------------------------------------------------------
管理员审核
----------------------------------------------------------------------------------------------------------------------------------------------
'''


# def check(request, u, p):
#     try:
#         content = {}
#         checkName = request.GET.get('name')
#         checkPassword = request.GET.get('password')
#         # 判断用户名和密码是否正确-start
#         isRight = False
#         oneuser = Manage.objects.filter(user=u)
#         if oneuser.count() > 0:
#             for i in oneuser:
#                 if i.password == p:
#                     isRight = True
#         # 判断用户名和密码是否正确-end
#     except Exception as e:
#         return errorFunc(request, e, sys._getframe().f_lineno)
#     if isRight:
#         if(request.method == "POST"):
#             try:
#                 inputBtn = request.POST.get("inputBtn")
#                 delBtn = request.POST.get("delBtn")
#                 # 录入信息-start
#                 if inputBtn != None and delBtn == None:
#                     requestDic = {
#                         "committerInformation": request.POST.get('committerInformation'),
#                         "committerUrl": request.POST.get('committerUrl'),
#                         #
#                         "reportQq": request.POST.get('reportQq'),
#                         "reportVx": request.POST.get('reportVx'),
#                         "reportSteam": request.POST.get('reportSteam'),
#                         "reportAliPay": request.POST.get('reportAliPay'),
#                         "reportMaxId": request.POST.get('reportMaxId'),
#                         "reportHeiBox": request.POST.get('reportHeiBox'),
#                         "reportTieBa": request.POST.get('reportTieBa'),
#                         "examineFlag": '1',  # 更新数据库状态，表示已经通过审核
#                     }
#                     for key, value in requestDic.items():  # 判断录入数据，若为空则在数据库中用none占位
#                         if value == '':
#                             requestDic[key] = 'none'
#                     oneInf = ToExamine.objects.filter(
#                         id=inputBtn).update(**requestDic)  # 存入数据库
#                     # 审核完成删除审核使用图片-start
#                     delInfoImg = ExamineImg.objects.filter(
#                         examine=inputBtn)
#                     if delInfoImg.count() > 0:
#                         delInfoImg.delete()
#                     # 审核完成删除审核使用图片-end
#                     # 保存审核结果至结果表-start
#                     saveDic = requestDic
#                     del saveDic['committerInformation']
#                     del saveDic['examineFlag']
#                     oneInfsave = Total.objects.create(**saveDic)
#                     oneInfsave.save()
#                     # 保存审核结果至结果表-end
#                     return HttpResponseRedirect('/check'+'/'+u+'/'+p+'/')
#                 # 录入信息-end
#                 # 删除信息-start
#                 elif inputBtn == None and delBtn != None:
#                     oneInf = ToExamine.objects.get(id=delBtn)
#                     # 保存审核结果至结果表-start
#                     delInfoImg = ExamineImg.objects.filter(examine=delBtn)
#                     if delInfoImg.count() > 0:
#                         delInfoImg.delete()
#                     # 保存审核结果至结果表-end
#                     oneInf.examineFlag = '2'  # 更新数据库状态，表示已经删除
#                     oneInf.save()
#                 # 删除信息-end
#             except Exception as e:
#                 return errorFunc(request, e, sys._getframe().f_lineno)
#         try:
#             oneInfo = ToExamine.objects
#             infList = []
#         except Exception as e:
#             return errorFunc(request, e, sys._getframe().f_lineno)
#         # 读取数据库数据显示html-start
#         if(oneInfo.filter(examineFlag='0')):
#             try:
#                 for i in oneInfo.filter(examineFlag='0'):
#                     infDict = {
#                         "committerInformation": i.committerInformation,
#                         "committerUrl": i.committerUrl,
#                         #
#                         "reportQq": i.reportQq,
#                         "reportVx": i.reportVx,
#                         "reportSteam": i.reportSteam,
#                         "reportAliPay": i.reportAliPay,
#                         "reportMaxId": i.reportMaxId,
#                         "reportHeiBox": i.reportHeiBox,
#                         "reportTieBa": i.reportTieBa,
#                         "id": i.id,
#                         "img": []
#                     }
#                     infoImg = ExamineImg.objects.filter(examine=i.id)
#                     for i in infoImg:
#                         infDict["img"].append(i.imgFile)
#                     infList.append(infDict)
#             except Exception as e:
#                 return errorFunc(request, e, sys._getframe().f_lineno)
#         try:
#             content['needCheck'] = infList
#             return render(request, 'check.html', content)
#         except Exception as e:
#             return errorFunc(request, e, sys._getframe().f_lineno)
#         # 读取数据库数据显示html-end
#     else:
#         return HttpResponse("无效的管理用户名或密码")


# '''
# ----------------------------------------------------------------------------------------------------------------------------------------------
# 搜索
# ----------------------------------------------------------------------------------------------------------------------------------------------
# '''


# def searchResults(request, searchContent, searchSelect, u, p):
#     try:
#         content = {
#             'flag': True  # 定义flag，检测是否为管理员登入
#         }
#         # 判断管理员用户名和密码是否正确-start
#         isRight = False
#         oneuser = Manage.objects.filter(user=u)
#         if oneuser.count() > 0:
#             for i in oneuser:
#                 if i.password == p:
#                     isRight = True
#         # 判断管理员用户名和密码是否正确-end
#     except Exception as e:
#         return errorFunc(request, e, sys._getframe().f_lineno)
#     # 管理员登入额外操作-start
#     if isRight:
#         try:
#             content['flag'] = False
#             if request.method == "POST":
#                 inputBtn = request.POST.get("inputBtn")
#                 delBtn = request.POST.get("delBtn")
#                 # 修改信息并保存-start
#                 if inputBtn != None and delBtn == None:
#                     # 更新审核表
#                     requestDic = {
#                         "committerUrl": request.POST.get('committerUrl'),
#                         #
#                         "reportQq": request.POST.get('reportQq'),
#                         "reportVx": request.POST.get('reportVx'),
#                         "reportSteam": request.POST.get('reportSteam'),
#                         "reportAliPay": request.POST.get('reportAliPay'),
#                         "reportMaxId": request.POST.get('reportMaxId'),
#                         "reportHeiBox": request.POST.get('reportHeiBox'),
#                         "reportTieBa": request.POST.get('reportTieBa'),
#                         "delete": '0',
#                     }
#                     for key, value in requestDic.items():
#                         if value == '':
#                             requestDic[key] = 'none'
#                     saveDic = requestDic
#                     del saveDic['delete']
#                     oneInf = Total.objects.filter(
#                         id=inputBtn).update(**saveDic)  # 修改数据库
#                     return HttpResponseRedirect('/res/'+searchContent+'/'+searchSelect+'/'+u+'/'+p+'/')
#                 # 修改信息并保存-end
#                 # 删除信息-start
#                 elif inputBtn == None and delBtn != None:
#                     oneInf = Total.objects.get(id=delBtn)
#                     oneInf.delete = '1'
#                     oneInf.save()
#                 # 删除信息-end
#         except Exception as e:
#             return errorFunc(request, e, sys._getframe().f_lineno)
#     # 管理员登入额外操作-end
# # 普通显示-start
#     else:
#         content['flag'] = True
#     resList = []
#     # 未指定搜索类型-start
#     if searchSelect == 'none':
#         try:
#             noneList = []
#             noneList.append(Total.objects.filter(
#                 reportQq=searchContent, delete='0'))
#             noneList.append(Total.objects.filter(
#                 reportVx=searchContent, delete='0'))
#             noneList.append(Total.objects.filter(
#                 reportSteam=searchContent, delete='0'))
#             noneList.append(Total.objects.filter(
#                 reportAliPay=searchContent, delete='0'))
#             noneList.append(Total.objects.filter(
#                 reportMaxId=searchContent, delete='0'))
#             noneList.append(Total.objects.filter(
#                 reportHeiBox=searchContent, delete='0'))
#             noneList.append(Total.objects.filter(
#                 reportTieBa=searchContent, delete='0'))
#             for j in noneList:
#                 for i in j:
#                     infDict = {
#                         "committerUrl": i.committerUrl,
#                         #
#                         "reportQq": i.reportQq,
#                         "reportVx": i.reportVx,
#                         "reportSteam": i.reportSteam,
#                         "reportAliPay": i.reportAliPay,
#                         "reportMaxId": i.reportMaxId,
#                         "reportHeiBox": i.reportHeiBox,
#                         "reportTieBa": i.reportTieBa,
#                         "id": i.id,
#                     }
#                     resList.append(infDict)
#             content['res'] = resList
#         except Exception as e:
#             return errorFunc(request, e, sys._getframe().f_lineno)
#     # 未指定搜索类型-end
#     # 选择搜索内容搜索-start
#     else:
#         try:
#             oneInfList = []
#             if searchSelect == 'qq':
#                 oneInfList.append(Total.objects.filter(
#                     reportQq=searchContent, delete='0'))
#             elif searchSelect == 'vx':
#                 oneInfList.append(Total.objects.filter(
#                     reportVx=searchContent, delete='0'))
#             elif searchSelect == 'steam':
#                 oneInfList.append(Total.objects.filter(
#                     reportSteam=searchContent, delete='0'))
#             elif searchSelect == 'alipay':
#                 oneInfList.append(Total.objects.filter(
#                     reportAliPay=searchContent, delete='0'))
#             elif searchSelect == 'max':
#                 oneInfList.append(Total.objects.filter(
#                     reportMaxId=searchContent, delete='0'))
#             elif searchSelect == 'hei':
#                 oneInfList.append(Total.objects.filter(
#                     reportHeiBox=searchContent, delete='0'))
#             elif searchSelect == 'tieba':
#                 oneInfList.append(Total.objects.filter(
#                     reportTieBa=searchContent, delete='0'))
#             elif searchSelect == 'id':
#                 if searchContent.isdigit():
#                     oneInfList.append(Total.objects.filter(
#                         id=searchContent, delete='0'))
#             for j in oneInfList:
#                 for i in j:
#                     infDict = {
#                         "committerUrl": i.committerUrl,
#                         #
#                         "reportQq": i.reportQq,
#                         "reportVx": i.reportVx,
#                         "reportSteam": i.reportSteam,
#                         "reportAliPay": i.reportAliPay,
#                         "reportMaxId": i.reportMaxId,
#                         "reportHeiBox": i.reportHeiBox,
#                         "reportTieBa": i.reportTieBa,
#                         "id": i.id,
#                     }
#                     resList.append(infDict)
#             content['res'] = resList
#         except Exception as e:
#             return errorFunc(request, e, sys._getframe().f_lineno)
#     # 选择搜索内容搜索-end
# # 普通显示-end
#     return render(request, 'res.html', content)


# '''
# ----------------------------------------------------------------------------------------------------------------------------------------------
# 404
# ----------------------------------------------------------------------------------------------------------------------------------------------
# '''


# def page_not_found(request, exception):
#     return render(request, '404.html')


# '''
# ----------------------------------------------------------------------------------------------------------------------------------------------
# 500
# ----------------------------------------------------------------------------------------------------------------------------------------------
# '''


# def page_error(request, exception):
#     return render(request, '500.html', {"error": "normalError", "erLine": 0})


# '''
# ----------------------------------------------------------------------------------------------------------------------------------------------
# 感谢
# ----------------------------------------------------------------------------------------------------------------------------------------------
# '''


# def thank(request):
#     try:
#         content = {
#             "thanks": [],
#         }
#         thanksInf = Thanks.objects.all()
#         # 读取感谢列表-start
#         for i in thanksInf:
#             thankDict = {
#                 "name": i.name,
#                 "url": i.thanksUrl,
#             }
#             content['thanks'].append(thankDict)
#         # 读取感谢列表-end
#     except Exception as e:
#         return errorFunc(request, e, sys._getframe().f_lineno)
#     return render(request, 'thank.html', content)


# '''
# ----------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------
# API
# ----------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------------------------
# '''


# def useApi(request, content):
#     contentJson = {
#         "code": 0,
#     }
#     # 数据库信息及网站基本信息-start
#     if content == 'databaseBasicInformation':
#         contentJson["code"] = 1
#         nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#         contentJson["databaseBasicInformation"] = {
#             "time": nowTime,
#             "Total": {
#                 "note": "总数据库相关信息",
#                 "exist": str(Total.objects.filter(delete="0").count()),
#                 "delete": str(Total.objects.filter(delete="1").count()),
#             },
#             "Examine": {
#                 "note": "审核数据库相关信息",
#                 "noCheck": str(Total.objects.filter(delete="0").count()),
#                 "checkFin": str(Total.objects.filter(delete="1").count()),
#                 "delete": str(Total.objects.filter(delete="2").count()),
#             },
#             "webInf": {
#                 "note": "网站信息",
#                 "visits": str(Statistics.objects.get(id=1).visits),
#                 "search": str(Statistics.objects.get(id=1).search),
#                 "upload": str(Statistics.objects.get(id=1).upload),
#             }
#         }
#         return JsonResponse(contentJson, json_dumps_params={'ensure_ascii': False}, content_type="application/json,charset=utf-8")
#     # 数据库信息及网站基本信息-end
#     else:
#         return JsonResponse(contentJson, json_dumps_params={'ensure_ascii': False}, content_type="application/json,charset=utf-8")
