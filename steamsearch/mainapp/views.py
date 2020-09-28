from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from mainapp.models import *
import re
import time
import sys

import traceback
import demjson
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
                if searchContent == '':  # 搜索为空刷新主页
                    return redirect('index')
                else:  # url反转搜索内容
                    return redirect(reverse('results', kwargs={'searchContent': str(searchContent)}))
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
                return errorFunc(request, e, sys._getframe().f_lineno)

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
        try:
            # 查看详细内容-start
            if request.method == 'POST':
                contentId = request.POST.get('contentBtn')
                return redirect(reverse('content', kwargs={'ID': str(contentId)}))
            # 查看详细内容-end
        except Exception as e:
            return errorFunc(request, e, sys._getframe().f_lineno)
        # 显示内容-start
        oneInfList = []  # 读取数据库列表
        resList = []  # 返回前端数据列表
        oneInfList.append(People.objects.filter(name=searchContent))
        for j in oneInfList:
            for i in j:
                infDict = {
                    "name": i.name,
                    "sex": '',
                    "birthdayY": '',
                    "birthdayM": '',
                    "birthdayD": '',
                    "height": i.weight,
                    "weight": i.height,
                    "timeLY": '',
                    "timeLM": '',
                    "timeLD": '',
                    "timeLH": '',
                    "timeLMin": '',
                    "site": i.site,
                    "text": i.text,
                    "kinName": i.kinName,
                    "kinLink": i.kinLink,
                    "img": [],
                    "id": i.id,
                }
                for key, value in infDict.items():
                    if value == "none":
                        infDict[key] = '未知'
                infoImg = PeopleImg.objects.filter(onePeople=i.id)
                if len(infoImg) > 0:
                    infDict["img"].append(infoImg[0].imgFile)
                # 处理性别-start
                if i.sex == "nan":
                    infDict['sex'] = "男"
                elif i.sex == "nv":
                    infDict['sex'] = "女"
                else:
                    infDict['sex'] = "未知/其他"
                # 处理性别-end
                # 处理生日-start
                birList = str(i.birthday).split('$')
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
                # 处理生日-end
                # 处理走失日期-start
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
                # 处理走失日期-end
                resList.append(infDict)
        content['res'] = resList
        # 显示内容-end
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)

    # 搜索名字-end
    return render(request, 'res.html', content)


'''
----------------------------------------------------------------------------------------------------------------------------------------------
详细信息
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def oneContent(request, ID):
    try:
        i = People.objects.filter(id=ID).first()
        infDict = {
            "name": i.name,
            "sex": '',
            "birthdayY": '',
            "birthdayM": '',
            "birthdayD": '',
            "height": i.weight,
            "weight": i.height,
            "timeLY": '',
            "timeLM": '',
            "timeLD": '',
            "timeLH": '',
            "timeLMin": '',
            "site": i.site,
            "text": i.text,
            "kinName": i.kinName,
            "kinLink": i.kinLink,
            "img": [],
            "id": i.id,
        }
        for key, value in infDict.items():
            if value == "none":
                infDict[key] = '未知'
        infoImg = PeopleImg.objects.filter(onePeople=i.id)
        for j in infoImg:
            infDict["img"].append(j.imgFile)
        # 处理性别-start
        if i.sex == "nan":
            infDict['sex'] = "男"
        elif i.sex == "nv":
            infDict['sex'] = "女"
        else:
            infDict['sex'] = "未知/其他"
        # 处理性别-end
        # 处理生日-start
        birList = str(i.birthday).split('$')
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
        # 处理生日-end
        # 处理走失日期-start
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
        # 处理走失日期-end
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)
    return render(request, 'content.html', infDict)


# '''
# ----------------------------------------------------------------------------------------------------------------------------------------------
# 管理员审核
# ----------------------------------------------------------------------------------------------------------------------------------------------
# '''
# def check(request):
#     content={}
#     try:
#         cookielog = request.session.get('islog')
#         if cookielog == "1":#成功进入
#             pass
#         elif cookielog != "1":
#             return redirect("manager")
#     except Exception as e:
#         return errorFunc(request, e, sys._getframe().f_lineno)
#     return render(request, 'check.html',content)

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


'''
----------------------------------------------------------------------------------------------------------------------------------------------
404
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def page_not_found(request, exception):
    return render(request, '404.html')


'''
----------------------------------------------------------------------------------------------------------------------------------------------
500
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def page_error(request, exception):
    return render(request, '500.html', {"error": "normalError", "erLine": 0})


'''
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
API
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def apidoc(request):
    return render(request, "apidoc.html")


def useApi(request, content):
    contentJson = {
        "code": 0,  # 1为正常，0为无次api，-1为报错
    }
    try:
        # 数据库信息及网站基本信息-start
        if content == 'basicIinformation':
            contentJson["code"] = 1
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            contentJson["basicinformation"] = {
                "time": nowTime,
                "Total": {
                    "note": "失联人员统计信息数量",
                    "exist": str(People.objects.all().count()),
                },
                "webInf": {
                    "note": "网站信息",
                    "visits": str(Statistics.objects.get(id=1).visits),
                    "search": str(Statistics.objects.get(id=1).search),
                    "upload": str(Statistics.objects.get(id=1).upload),
                }
            }
            return JsonResponse(contentJson, json_dumps_params={'ensure_ascii': False}, content_type="application/json,charset=utf-8")
        # 数据库信息及网站基本信息-end
    except Exception as e:
        contentJson = {}
        contentJson['code'] = -1
        contentJson['error'] = str(e)
        return JsonResponse(contentJson, json_dumps_params={'ensure_ascii': False}, content_type="application/json,charset=utf-8")
    try:
        # 查询记录信息-start
        if content == 'getinformation':
            contentJson["code"] = 1
            if request.method == 'POST':
                post = demjson.decode(request.body)
                name = post["name"]
            nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            contentJson["getinformation"] = {
                "time": nowTime,
                "content": [],
            }
            oneInfList = []
            oneInfList.append(People.objects.filter(name=name))
            for j in oneInfList:
                for i in j:
                    infDict = {
                        "name": i.name,
                        "sex": i.sex,
                        "birthday": i.birthday,
                        "height": i.weight,
                        "weight": i.height,
                        "timeL": i.timeL,
                        "site": i.site,
                        "text": i.text,
                        "kinName": i.kinName,
                        "kinLink": i.kinLink,
                        "img": [],
                    }
                    infoImg = PeopleImg.objects.filter(onePeople=i.id)
                    for m in infoImg:
                        infDict["img"].append(
                            "www.jhc.cool/media/"+str(m.imgFile))
                    contentJson["getinformation"]["content"].append(infDict)
            return JsonResponse(contentJson, json_dumps_params={'ensure_ascii': False}, content_type="application/json,charset=utf-8")
        # 数查询记录信息-end
    except Exception as e:
        contentJson = {}
        contentJson['code'] = -1
        contentJson['error'] = str(e)
        return JsonResponse(contentJson, json_dumps_params={'ensure_ascii': False}, content_type="application/json,charset=utf-8")


'''
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
论坛
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------------------
'''

'''
----------------------------------------------------------------------------------------------------------------------------------------------
注册
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def register(request):
    content = {
        "mess": "",
    }
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            userpass = request.POST.get('userpass')
            userpass2 = request.POST.get('userpass2')
            useremail = request.POST.get('email')
            if len(userpass) > 0 or len(userpass2) > 0 or len(userpass) > 0 or len(useremail) > 0:
                getuser = User.objects.filter(name=username)
                if userpass != userpass2:
                    content["mess"] = "两次输入密码不一致"
                    return render(request, 'register.html', content)
                elif getuser.count() > 0:
                    content["mess"] = "该账号已经注册，请直接登陆"
                    return render(request, 'register.html', content)
                else:
                    oneuser = User.objects.create(
                        name=username, password=userpass, email=useremail)
                    oneuser.save()
                    request.session['user'] = username
                    return redirect('bbsindex')
            else:
                content["mess"] = "有未填项"
                return render(request, 'register.html', content)
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)

    return render(request, 'register.html', content)


'''
----------------------------------------------------------------------------------------------------------------------------------------------
登陆
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def login(request):
    content = {
        "mess": "",
    }
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            userpass = request.POST.get('userpass')
            if len(userpass) > 0 and len(username) > 0:
                getuser = User.objects.filter(name=username)
                if getuser.count() < 0:
                    content["mess"] = "该用户不存在，请注册"
                    return render(request, 'login.html', content)
                elif getuser.first().password != userpass:
                    content["mess"] = "密码或用户名错误"
                    return render(request, 'login.html', content)
                else:
                    request.session['user'] = username
                    return redirect('bbsindex')
            else:
                content["mess"] = "有未填项"
                return render(request, 'login.html', content)
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)
    return render(request, 'login.html', content)


'''
----------------------------------------------------------------------------------------------------------------------------------------------
论坛主页
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def bbsindex(request):
    content = {
        "user": None,
        "res": []
    }
    try:
        cookielog = request.session.get('user')
        print(cookielog)
        if cookielog != None:
            content["user"] = cookielog
        # 显示内容-start
        getNews = News.objects.all()
        flag = 0
        for i in getNews:
            title = i.title
            contentLite = i.content
            if len(contentLite) > 80:
                contentLite = contentLite[:79]+"..."
            else:
                contentLite = contentLite
            dicts = {
                "title": i.title,
                "content": contentLite,
                "id": i.id,
            }
            content["res"].append(dicts)
            flag += 1
            if flag > 15:
                flag = 0
                break
        # 显示内容-end
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)
    return render(request, "bbsindex.html", content)


'''
----------------------------------------------------------------------------------------------------------------------------------------------
发帖
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def postnew(request):
    content = {
        "user": None
    }
    try:
        cookielog = request.session.get('user')
        print(cookielog)
        if cookielog != None:
            content["user"] = cookielog
            if request.method == 'POST':
                thisuser = User.objects.filter(name=cookielog).first()
                title = request.POST.get('title')
                contents = request.POST.get('content')
                oneNews = News.objects.create(
                    userid=thisuser, title=title, content=contents)
                for i in request.FILES.getlist("newsimg"):
                    checkImg = newsImg.objects.create(
                        oneNews=oneNews, imgFile=i)  # 存储上传图片
                    checkImg.save()
                oneNews.save()
                return redirect('bbsindex')
        else:
            return redirect('login')
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)
    return render(request, "postnews.html")


'''
----------------------------------------------------------------------------------------------------------------------------------------------
发帖
----------------------------------------------------------------------------------------------------------------------------------------------
'''


def bbscontent(request, content):
    contents = {}
    try:
        pass
        # 显示内容-start
        oneNews = News.objects.filter(id=content).first()
        contents["title"] = oneNews.title
        contents["content"] = oneNews.content
        contents["img"] = []
        infoImg = newsImg.objects.filter(oneNews=content)
        for i in infoImg:
            contents["img"].append(i.imgFile)
        # 显示内容-end
    except Exception as e:
        return errorFunc(request, e, sys._getframe().f_lineno)
    return render(request, "bbscontent.html", contents)
