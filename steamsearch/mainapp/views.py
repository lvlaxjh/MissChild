from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mainapp.models import *
import re
import time
import sys

import traceback

'''
----------------------------------------------------------------------------------------------------------------------------------------------
功能函数
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def errorFunc(request, e,):
    print("********************************500-Error-start********************************")
    print(str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
    print("errorContent:    "+str(e))
    print("********************************500-Error-end********************************")
    return render(request, '500.html', {"error": e})


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
        return errorFunc(request, repr(e))
    if request.method == 'POST':
        try:
            searchButton = request.POST.get('searchButton')
            subButton = request.POST.get('subInf')
        except Exception as e:
            return errorFunc(request, repr(e))
        if searchButton == 'searchButton':
            try:
                # 站内统计-start
                stat = Statistics.objects.get(id=1)
                stat.search += 1
                stat.save()
                # 站内统计-end
            except Exception as e:
                return errorFunc(request, repr(e))
            try:
                # 搜索-start
                searchContent = request.POST.get('searchContent')
                if searchContent == '':  # 搜索为空刷新主页
                    return redirect('index')
                else:  # url反转搜索内容
                    return redirect(reverse('results', kwargs={'searchContent': str(searchContent)}))
                # 搜索-end
            except Exception as e:
                return errorFunc(request, repr(e))
        # 上传信息-start
        if subButton == 'subInf':
            try:
                # 站内统计-start
                stat = Statistics.objects.get(id=1)
                stat.upload += 1
                stat.save()
                # 站内统计-end
            except Exception as e:
                return errorFunc(request, repr(e))
            try:
                requestDic = {
                    "name": request.POST.get('missCName'),
                    "sex": request.POST.get('missCsex'),
                    "height": request.POST.get('missCheight'),
                    "weight": request.POST.get('missCweight'),
                    "birthday": request.POST.get('missCbirthdayY')+"$"+request.POST.get('missCbirthdayM')+"$"+request.POST.get('missCbirthdayD'),
                    "timeL": request.POST.get('missCtimeY')+"$"+request.POST.get('missCtimeM')+"$"+request.POST.get('missCtimeD')+"$"+request.POST.get('missCtimeH')+"$"+request.POST.get('missCtimeMin'),
                    "site": request.POST.get('missCsite'),
                    "text": request.POST.get('missCtext'),
                    "kinName": request.POST.get('kinName'),
                    "kinLink": request.POST.get('kinLink'),
                }
                for key, value in requestDic.items():  # 若上传信息为空则用none占位
                    if key == 'birthday' and value == '':
                        requestDic[key] = "none$none$none"
                    elif key == 'timeL' and value == '':
                        requestDic[key] = "none$none$none$none$none"
                    elif (key != 'birthday' or key != 'timeL') and len(value) == 0:
                        requestDic[key] = 'none'
                oneInf = People.objects.create(**requestDic)  # 数据库增加一条数据
                for i in request.FILES.getlist("missCimg"):
                    checkImg = PeopleImg.objects.create(
                        onePeople=oneInf, imgFile=i)  # 存储上传图片
                    checkImg.save()
                oneInf.save()
                return redirect('index')  # 上传完成后刷新页面（防止了刷新页面重复提交表单）
            except Exception as e:
                return errorFunc(request, repr(e))
        # 上传信息end--------------------------------------------------------------
    return render(request, 'index.html', content)


'''
----------------------------------------------------------------------------------------------------------------------------------------------
搜索
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def searchResults(request, searchContent):
    content = {}
    # 搜索名字-start
    try:
        oneInfList = []#读取数据库列表
        resList = []#返回前端数据列表
        oneInfList.append(People.objects.filter(name=searchContent))
        for j in oneInfList:
            for i in j:
                infDict = {
                    "name": i.name,
                    "sex": '',
                    "birthdayY": '',
                    "birthdayM": '',
                    "birthdayD": '',
                    "height": '',
                    "weight": '',
                    "timeLY": '',
                    "timeLM": '',
                    "timeLD": '',
                    "timeLH": '',
                    "timeLMin": '',
                    "site": i.site,
                    "text": i.text,
                    "kinName":i.kinName,
                    "kinLink":i.kinLink,
                    "img":[],
                    "id": i.id,
                }
                # for i in infoImg:
#                         infDict["img"].append(i.imgFile)
                infoImg = PeopleImg.objects.filter(onePeople=i.id)
                for n in infoImg:
                    infDict["img"].append(n.imgFile)
                #处理性别-start
                if i.sex == "nan":
                    infDict['sex']="男"
                elif i.sex == "nv":
                    infDict['sex']="女"
                else:
                    infDict['sex']="未知/其他"
                #处理性别-end
                #处理生日-start
                birList =  str(i.birthday).split('$')
                if birList[0] != "none":
                    infDict['birthdayY'] = birList[0]
                else:
                    infDict['birthdayY'] = '未知'
                if birList[1] != "none":
                    infDict['birthdayM'] = birList[1]
                else:
                    infDict['birthdayM'] = '未知'
                if birList[2] != "none":
                    infDict['birthdayD'] = birList[2]
                else:
                    infDict['birthdayD'] = '未知'
                #处理生日-end
                #处理走失日期-start
                missT = str(i.timeL).split('$')
                if missT[0] != 'none':
                    infDict['timeLY'] = missT[0]
                else:
                    infDict['timeLY'] = '未知'
                if missT[1] != 'none':
                    infDict['timeLM'] = missT[1]
                else:
                    infDict['timeLM'] = '未知'
                if missT[2] != 'none':
                    infDict['timeLD'] = missT[2]
                else:
                    infDict['timeLD'] = '未知'
                if missT[3] != 'none':
                    infDict['timeLH'] = missT[3]
                else:
                    infDict['timeLH'] = '未知'
                if missT[4] != 'none':
                    infDict['timeLMin'] = missT[4]
                else:
                    infDict['timeLMin'] = '未知'
                #处理走失日期-end
                resList.append(infDict)
        content['res'] = resList
    except Exception as e:
        return errorFunc(request, repr(e))
    # 搜索名字-end
    return render(request, 'res.html', content)

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
