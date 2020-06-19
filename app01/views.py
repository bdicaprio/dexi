from django.shortcuts import render
from anaconda_navigator.utils.py3compat import request
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from app01 import models
from _cffi_backend import string
from django.db import connection
import json
from builtins import dict, id
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.utils.encoding import repercent_broken_unicode
from django.contrib.auth.hashers import make_password
from io import BytesIO
import datetime
from openpyxl import load_workbook
from openpyxl import Workbook
from django.http import StreamingHttpResponse
import os
from numpy.ma.core import getdata
from _ast import Dict, If
from app01.models import company
from pickle import DICT
from pylint.test.functional import unnecessary_pass

# Create your views here.


def login(request):
    return render(request,'login.html',{})

def logout(request):
    request.session.flush()
    return render(request,'login.html',{})

#验证
def authlogin(request,*args,**kwargs):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            
            request.session['username'] = username
            return HttpResponseRedirect ("/index/", { } )                 
        else:      
            return render(request,'login.html',{'error':'用户名或密码错误',})
    
    
#获取index页面所有数据   
def index(request,*args,**kwargs):
    username = request.session.get('username','anybody') 
    resultId = models.userProfile.objects.values("id").filter(username=username)
    for i in resultId:
        id = i['id']    
             
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)        
    for i in superuser:
        lsSuperuser = str(i['is_superuser'])
        

    if lsSuperuser == 'True': #如果是管理员账号,性别和学历返回空
        resultStatistics = {"corporateGender":0,"education":0,} 
        return render (
            request,
            "index.html", 
            {
            "resultStatistics":resultStatistics, 
            "username":username, 
            "superuser":superuser,                                  
            }  
        ) 
    else: 
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
        for i in resultCompanyNameId:
            companyNameId = str(i['id'])      
        try: #普通用户填过数据返回数据
            
            resultStatistics = models.statistics.objects.filter(company_id=companyNameId)
            if resultStatistics.exists:
                resultStatistics = models.statistics.objects.get(company_id=companyNameId)
            resultCompany = models.statistics.objects.filter(company_id=companyNameId)
            if resultCompany.exists:
                resultCompany = models.statistics.objects.get(company_id=companyNameId)  
            resultEconomic = models.statistics.objects.filter(company_id=companyNameId)
            if resultEconomic.exists:
                resultEconomic = models.statistics.objects.get(company_id=companyNameId)  
            resultPersonnel = models.statistics.objects.filter(company_id=companyNameId)
            if resultPersonnel.exists:
                resultPersonnel = models.statistics.objects.get(company_id=companyNameId) 
            resultActivities = models.statistics.objects.filter(company_id=companyNameId)
            if resultActivities.exists:
                resultActivities = models.statistics.objects.get(company_id=companyNameId)                                                                  


            return render (
                request,
                "index.html", 
                {
                "resultStatistics":resultStatistics, 
                "resultCompany":resultCompany, 
                "resultEconomic":resultEconomic, 
                "resultPersonnel":resultPersonnel, 
                "resultActivities":resultActivities, 
                "username":username,
                "superuser":superuser,                       
               } 
            )       
        except: #普通用户没填过数据         
            resultStatistics = {"corporateGender":0,"education":0,} #第一次登入传传默认值      
            
                  
        return render (
            request,
            "index.html", 
            {
            "resultStatistics":resultStatistics, 
            "username":username, 
            "superuser":superuser,                                  
            }
        )
        
def catprojectlist(request): 
    sql = ' '
    sql_count = ''
    id = ''
    CompanyNameId = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')    
    companyname = request.GET.get('companyname')
    print(companyname)        
    
    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    for i in resultId:
        companyNameId = str(i['id'])  
        
    print(companyNameId)
    start = str((int(p)-1) * int(l))
    end = str(l)    
    
    print(companyNameId,start,end)  
    sql = 'select id,company_id,projectName,projectFrom,developmentForm,achievement,economicGoals,activityType,date_format(startTime,"%Y-%m-%d %T") as startTime,date_format(endTime,"%Y-%m-%d %T") as endTime,personnel,time,stage,funds,capital  from app01_projects  where  company_id = ' +   companyNameId   +  ' limit '  +  start + ','  + end
    print(sql)
    sql_count = 'select count(*)  from  app01_projects where company_id = ' + companyNameId        

    cursor = connection.cursor()
    cursor.execute(sql)
    rawData = cursor.fetchall()    
    col_names = [desc[0] for desc in cursor.description]
    result = []
    
    for row in rawData:
        objDict = {}
        
        for index, value in enumerate(row):           
            objDict[col_names[index]] = value       
    
        result.append(objDict)
    cursor.execute(sql_count)
    count = cursor.fetchall()
    count = count[0][0]      
    dict = {"code":0,"msg":"","count":count,"data":result}
    return HttpResponse(json.dumps(dict), content_type="application/json")          
    
#获取项目表格数据
def getPojectList(request):
    sql = ''
    sql_count = ''
    id = ''
    CompanyNameId = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')      
    username = request.session.get('username','anybody') 
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperuser = str(i['is_superuser'])        
    if lsSuperuser == 'True':
        dict = {"code":0,"msg":"","count":0,"data":""}
        return HttpResponse(json.dumps(dict), content_type="application/json")
    else:    
        projectName = getData.get('projectName') #搜索接受项目名称
        print("projectName",projectName)
        start = str((int(p)-1) * int(l))
        end = str(l)
        resultUsernameId = models.userProfile.objects.values("id").filter(username=username)
        for i in resultUsernameId:
            id = str(i['id']) 
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
        for i in resultCompanyNameId:
            CompanyNameId = str(i['id'])            
        if (str(projectName)) == 'None':  #搜索为空
            print("111111111111111111111111")
            sql = 'select id,company_id,projectName,projectFrom,developmentForm,achievement,economicGoals,activityType,date_format(startTime,"%Y-%m-%d %T") as startTime,date_format(endTime,"%Y-%m-%d %T") as endTime,personnel,time,stage,funds,capital  from app01_projects  where  company_id = ' +   CompanyNameId   +  ' limit '  +  start + ','  + end
            print(sql)
            sql_count = 'select count(*)  from  app01_projects where company_id = ' + CompanyNameId
        elif(len(str(projectName)) == 0):   #搜索为空
            print("2222222222222222222222222222222")
            sql = 'select id,company_id,projectName,projectFrom,developmentForm,achievement,economicGoals,activityType,date_format(startTime,"%Y-%m-%d %T") as startTime,date_format(endTime,"%Y-%m-%d %T") as endTime,personnel,time,stage,funds,capital  from app01_projects  where  company_id = ' +   CompanyNameId   +  ' limit '  +  start + ','  + end
            print(sql)
            sql_count = 'select count(*)  from  app01_projects  where company_id  = ' + CompanyNameId        
        else :   #搜索
            sql = 'select id,company_id,projectName,projectFrom,developmentForm,achievement,economicGoals,activityType,date_format(startTime,"%Y-%m-%d %T") as startTime,date_format(endTime,"%Y-%m-%d %T") as endTime,personnel,time,stage,funds,capital  from app01_projects  where  company_id = ' +   CompanyNameId  + ' and   projectName like '  +  " '%"    +   projectName  + "%' " +  ' limit '  +  start + ','  + end
            print(sql)
            sql_count = 'select count(*)  from app01_projects  where  company_id = ' +   CompanyNameId  + ' and  projectName   like '  +  " '%"    +   projectName  + "%' " +  ' limit '  +  start + ','  + end
            print(sql)
            print(sql_count)
            
        cursor = connection.cursor()
        cursor.execute(sql)
        rawData = cursor.fetchall()    
        col_names = [desc[0] for desc in cursor.description]
        result = []
        
        for row in rawData:
            objDict = {}
            
            for index, value in enumerate(row):           
                objDict[col_names[index]] = value       
        
            result.append(objDict)
        cursor.execute(sql_count)
        count = cursor.fetchall()
        count = count[0][0]      
        dict = {"code":0,"msg":"","count":count,"data":result}
        return HttpResponse(json.dumps(dict), content_type="application/json")
    
    
def getprojectlisttmp(request):  
    sql = ''
    sql_count = ''
    id = ''
    CompanyNameId = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')  
    companyname = request.GET.get('companyname')
    print(companyname)
    username = request.session.get('username','anybody')
#    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
#    for i in superuser:
#        lsSuperuser = str(i['is_superuser'])        
#    if lsSuperuser == 'True':
#        dict = {"code":0,"msg":"","count":0,"data":""}
#        return HttpResponse(json.dumps(dict), content_type="application/json")
#    else:    
#        projectName = getData.get('projectName') #搜索接受项目名称
    start = str((int(p)-1) * int(l))
    end = str(l)
    try:
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyname)  
        for i in resultCompanyNameId:
            companyNameId = str(i['id'])
    


        sql = 'select id,company_id,projectName,projectFrom,developmentForm,achievement,economicGoals,activityType,date_format(startTime,"%Y-%m-%d %T") as startTime,date_format(endTime,"%Y-%m-%d %T") as endTime,personnel,time,stage,funds,capital  from app01_projects  where  company_id = ' +   companyNameId   +  ' limit '  +  start + ','  + end
        print(sql)
        sql_count = 'select count(*)  from  app01_projects where company_id = ' + companyNameId
        cursor = connection.cursor()
        cursor.execute(sql)
        rawData = cursor.fetchall()    
        col_names = [desc[0] for desc in cursor.description]
        result = []
    
        for row in rawData:
            objDict = {}
            
            for index, value in enumerate(row):           
                objDict[col_names[index]] = value       
        
            result.append(objDict)
        cursor.execute(sql_count)
        count = cursor.fetchall()
        count = count[0][0]      
        dict = {"code":0,"msg":"","count":count,"data":result}
        return HttpResponse(json.dumps(dict), content_type="application/json")
    except:
        dict = {"code":0,"msg":"","count":0,"data":""}
        return HttpResponse(json.dumps(dict), content_type="application/json")


def addStatistics(request):
    postData = request.POST
    username = request.session.get('username','anybody') 
    resultId = models.userProfile.objects.values("id").filter(username=username)
    statisticsId = postData.get('statisticsId')
    print(statisticsId)
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']

    if lsSuperUser is  True:  #管理员添加
        
        dict = {
            'organizationCode' : postData.get('organizationCode'),
            'areaNumber' : postData.get('areaNumber'),
            'enterpriseName' : postData.get('enterpriseName'),
            'natureOfCorporation' : postData.get('natureOfCorporation'),
            'corporateGender' : postData.get('corporateGender'),
            'birthday' : postData.get('birthday'),
            'education' : postData.get('education'),
            'address' : postData.get('address'),
            'postalCode' : postData.get('postalCode'),
            'registeredAddress' : postData.get('registeredAddress'),
            'manager' : postData.get('manager'),
            'telephone' : postData.get('telephone'),       
            'fax' : postData.get('fax'),
            'statisticalControlOfficer' : postData.get('statisticalControlOfficer'),
            'preparedBy' : postData.get('preparedBy'),
            'preparedByTelephone' : postData.get('preparedByTelephone'),
            'fillingTime' : postData.get('fillingTime'),
            'email' : postData.get('email'),
            'url' : postData.get('url'),
            'preparedByMobilephone' : postData.get('preparedByMobilephone'),
        }
        print("11111111111111111111111")
        models.statistics.objects.filter(id=statisticsId).update(**dict) 
        print("22222222222222222222222222")
    else:     #普通用户根据companyInfo找到公司名称的id
        id = ''
        for i in resultId:
            id = i['id']    
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
        for i in resultCompanyNameId:
                companyNameId = str(i['id'])             
        dict = {
            'organizationCode' : postData.get('organizationCode'),
            'areaNumber' : postData.get('areaNumber'),
            'enterpriseName' : postData.get('enterpriseName'),
            'natureOfCorporation' : postData.get('natureOfCorporation'),
            'corporateGender' : postData.get('corporateGender'),
            'birthday' : postData.get('birthday'),
            'education' : postData.get('education'),
            'address' : postData.get('address'),
            'postalCode' : postData.get('postalCode'),
            'registeredAddress' : postData.get('registeredAddress'),
            'manager' : postData.get('manager'),
            'telephone' : postData.get('telephone'),       
            'fax' : postData.get('fax'),
            'statisticalControlOfficer' : postData.get('statisticalControlOfficer'),
            'preparedBy' : postData.get('preparedBy'),
            'preparedByTelephone' : postData.get('preparedByTelephone'),
            'fillingTime' : postData.get('fillingTime'),
            'email' : postData.get('email'),
            'url' : postData.get('url'),
            'preparedByMobilephone' : postData.get('preparedByMobilephone'), 
            'company_id' : companyNameId,    
        }
        if models.statistics.objects.filter(company_id=companyNameId):
            models.statistics.objects.filter(company_id=companyNameId).update(**dict)
        else:
            models.statistics.objects.create(**dict)
    return render(
        request,
        "index.html", 
        {

        }                
    )
    
def addProject(request):   
    getData = request.GET
    id = getData.get('id')
    try:
        result = models.projects.objects.get(id=id)
        return render(
        request,
        "addproject.html", 
        {
            'result':result,
        }  
    )
    except:
        return render(request,"addproject.html",                
                {
                    
                }  
    )
        
        
def addProjectTmp(request):
    getData = request.GET
    id = getData.get('id')
    try:
        result = models.projects.objects.get(id=id)
        return render(
        request,
        "addprojecttmp.html", 
        {
            'result':result,
        }  
    )
    except:
        return render(request,"addprojecttmp.html",                
                {
                    
                }  
    )    
    
        
        
def saveProject(request):
    postData = request.POST
    username = request.session.get('username','anybody')     
#    companyName = request.POST.get('companyNameId')
    
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']

    if lsSuperUser is  True:  #管理员添加    
#        resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyName)  #管理员获取公司的id
#        for i in resultCompanyNameId:
#            companyNameId = str(i['id'])  
        try:    
            companyName = postData.get('companyNameId')
            print(companyName)  
            id = postData.get('id')
            
            resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyName)
            for i in resultCompanyNameId:
                companyNameId = str(i['id'])      
            print("111111111111111111111")            
            dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'company_id' : companyNameId, 
            }               
            models.projects.objects.filter(id=id).update(**dict) 
        except: 
            dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'company_id' : companyNameId, 
            }                        
            models.projects.objects.create(**dict) 
            
    else:
        resultId = models.userProfile.objects.values("id").filter(username=username)  #普通获取用户的id
        id = ''
        companyNameId = ''
        for i in resultId:
            id = i['id']   
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)  #普通用户获取公司的id
        for i in resultCompanyNameId:
            companyNameId = str(i['id'])       
        try:    
            id = postData.get('id')  
            print(id)     
            dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'company_id' : companyNameId, 
                'id': id,
            }            
            models.projects.objects.filter(id=id).update(**dict)          
        except:
            dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'company_id' : companyNameId, 
            }
            print(dict)
            models.projects.objects.create(**dict)    
     
         
    return render(
            request,
            "addproject.html", 
            {
    
            }                
        )
    
#管理员添加项目方法
def saveProjectTmp(request): 
    postData = request.POST
    username = request.session.get('username','anybody') 
    companyName = postData.get("companyName") #获取公司名称
    projectId = postData.get("id")  #获取项目id
    print(len(str(projectId)))
    print("projectId",projectId)
    dictError = {
        'companyName' : postData.get('companyName'),
    }
    if len(companyName) == 0:   #没有输公司名字
        print("1111111111111111111111111111")
        models.projectstmp.objects.create(**dictError)      #让程序报错           
    elif len(str(projectId)) == 0:  #没有项目id添加项目
        print("222222222222222222222222222222222")
        resultId = models.userProfile.objects.values("id").filter(username=username)  #获取用户的id
        for i in resultId:
            id = str(i['id'])   
        dictInfo = {
            'username_id': id,
            'companyname': companyName,
        }
        print(companyName)
        if models.companyInfo.objects.filter(companyname=companyName):  #如果公司已经添加过可以直接添加项目
            print("33333333333333333333333333333333")
            companyNameId = ''
            resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyName)  #获取公司的id
            for i in resultCompanyNameId:
                companyNameId = str(i['id'])       
            dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'company_id' : companyNameId, 
            }  
            print(dict)                       
            models.projects.objects.create(**dict)
            print("3456787uy65435")
        else:
            print("444444444444444444444444444444444")
            print(dictInfo)
            models.companyInfo.objects.create(**dictInfo)      #公司没有添加过先添加公司
            companyNameId = ''
            resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyName)  #获取公司的id
            for i in resultCompanyNameId:
                companyNameId = str(i['id'])         
            dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'company_id' : companyNameId, 
            }   

            models.projects.objects.create(**dict) 
    else:    
         #更新项目
        print("4555555555555555555555555555555555555")          
        dict = {
                'projectName' : postData.get('projectName'),
                'projectFrom' : postData.get('projectFrom'),
                'developmentForm' : postData.get('developmentForm'),
                'achievement' : postData.get('achievement'),
                'economicGoals' : postData.get('economicGoals'),
                'activityType' : postData.get('activityType'),
                'stage' : postData.get('stage'),
                'startTime' : postData.get('startTime'),
                'endTime' : postData.get('endTime'),
                'personnel' : postData.get('personnel'),
                'funds' : postData.get('funds'),
                'capital' : postData.get('capital'),
                'id': projectId,         
        }
        print(dict)                
        models.projects.objects.filter(id=projectId).update(**dict)   
    return render(
            request,
            "addprojecttmp.html", 
            {
                     
            }                
        )    
      
    

       
def addCompany(request):
    postData = request.POST.getlist('companyData[]')
    username = request.session.get('username','anybody') 
    companyId = request.POST.get('companyId')
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']

    if lsSuperUser is  True:#管理员添加   
        dict = {
           'qb07_2': postData[1],
           'qb07_3': postData[2],
           'qb08': postData[3],
           'qb21': postData[4],
           'qb22': postData[5],
           'qb101': postData[6],
           'qb03_0': postData[7],
           'qb03_1': postData[8],
           'qb04': postData[9],
           'qb04_0': postData[10],   
           'qb20_1': postData[11],
           'qb20': postData[12],
           'qb06': postData[13],
           'qb06_1': postData[15],
           'qb06_2': postData[16],
           'qb18': postData[17],
           'qb09': postData[18],
           'qb10': postData[19],
           'qb12': postData[20],
           'qb14': postData[21],  
           'qb14_1': postData[22],
           'qb14_2': postData[23],
           'qb15': postData[24],
           'qb15_1': postData[25],
           'qb15_2': postData[26],
           'qb15_3': postData[27],
           'qb15_4': postData[28],
           'qb15_5': postData[29],
           'qb16': postData[30],
           'qb16_1': postData[31], 
        }   
        print(dict)
        print(companyId)
        
        models.company.objects.filter(id=companyId).update(**dict)
        
    else:
        resultUsernameId = models.userProfile.objects.values("id").filter(username=username)
        for i in resultUsernameId:
            id = str(i['id']) 
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
        for i in resultCompanyNameId:
            companyNameId = str(i['id'])       
        dict = {
           'qb07_2': postData[1],
           'qb07_3': postData[2],
           'qb08': postData[3],
           'qb21': postData[4],
           'qb22': postData[5],
           'qb101': postData[6],
           'qb03_0': postData[7],
           'qb03_1': postData[8],
           'qb04': postData[9],
           'qb04_0': postData[10],   
           'qb20_1': postData[11],
           'qb20': postData[12],
           'qb06': postData[13],
           'qb06_1': postData[15],
           'qb06_2': postData[16],
           'qb18': postData[17],
           'qb09': postData[18],
           'qb10': postData[19],
           'qb12': postData[20],
           'qb14': postData[21],  
           'qb14_1': postData[22],
           'qb14_2': postData[23],
           'qb15': postData[24],
           'qb15_1': postData[25],
           'qb15_2': postData[26],
           'qb15_3': postData[27],
           'qb15_4': postData[28],
           'qb15_5': postData[29],
           'qb16': postData[30],
           'qb16_1': postData[31], 
           'company_id' : companyNameId,                      
        }
        if models.company.objects.filter(company_id=companyNameId):
    
            models.company.objects.filter(company_id=companyNameId).update(**dict)
        else:
            models.company.objects.create(**dict)    
        
    return render(
        request,
        "index.html", 
        {

       }
    )
    
  
def addEconomic(request):
   
    username = request.session.get('username','anybody')
    postData = request.POST.getlist('economicData[]')
    postDataContinues = request.POST.getlist('economicContinuesData[]') 
    economicId = request.POST.get('economicId')
    
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']
    if lsSuperUser is  True:  #管理员添加
        print("111111111111111111111111111")
        dict = {
           'qc02': postData[1],
           'qc02_05': postData[2],
           'qc55': postData[3],
           'qc06': postData[4],
           'qc06_1': postData[5],
           'qc06_2': postData[6],
           'qc06_3': postData[7],
           'qc06_4': postData[8],
           'qc07': postData[9],
           'qc09': postData[10],   
           'qc10': postData[11],
           'qc49': postData[12],
           'qc52': postData[13],
           'qc11': postData[14],
           'qc38': postData[15],
           'qc11_1': postData[16],
           'qc220': postData[17],
           'qc220_1': postData[18],
           'qc221': postData[19],
           'qc222': postData[20],  
           'qc223': postData[21],
           'qc223_2': postData[22],
           'qc223_3': postData[23],
           'qc224': postData[24],
           'qc228': postData[25],
           'qc229': postData[26],
           'qc225': postData[27],
           'qc233': postData[28],
           'qc232': postData[29],
           'qc120': postData[30],   
           'qc227': postData[31],   
           'qc230': postData[32],
           'qc234': postDataContinues[2],
           'qc12': postDataContinues[3],
           'qc231': postDataContinues[4],
           'qc13': postDataContinues[5],
           'qc14': postDataContinues[6],
           'qc16': postDataContinues[7],
           'qc17': postDataContinues[8],
           'qc18': postDataContinues[9],
           'qc20': postDataContinues[10],  
           'qc20_1': postDataContinues[11],
           'qc20_2': postDataContinues[12],
           'qc20_3': postDataContinues[13],
           'qc62': postDataContinues[14],
           'qc51': postDataContinues[15],
           'qc24': postDataContinues[16],
           'qc25': postDataContinues[17],
           'qc27_1': postDataContinues[18],
           'qc29': postDataContinues[19],
           'qc30': postDataContinues[20],    
           'qc65': postDataContinues[21],
           'qc61': postDataContinues[22],
           'qc30': postDataContinues[23],
           'qc31': postDataContinues[24],
           'qc33': postDataContinues[25],  
           'qc34': postDataContinues[26],
           'qc63': postDataContinues[27],
           'qc50': postDataContinues[28],
           'qc39': postDataContinues[29],
           'qc40': postDataContinues[30],
           'qc41': postDataContinues[31],  
           'QC226_1': postDataContinues[36],
           'QC226_2': postDataContinues[37],
           'QC226': postDataContinues[38], 
        }        
        models.economic.objects.filter(id=economicId).update(**dict)
    else:    
        username = request.session.get('username','anybody') 
        resultUsernameId = models.userProfile.objects.values("id").filter(username=username)
        for i in resultUsernameId:
            id = str(i['id']) 
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
        for i in resultCompanyNameId:
            companyNameId = str(i['id'])       
        dict = {
           'qc02': postData[1],
           'qc02_05': postData[2],
           'qc55': postData[3],
           'qc06': postData[4],
           'qc06_1': postData[5],
           'qc06_2': postData[6],
           'qc06_3': postData[7],
           'qc06_4': postData[8],
           'qc07': postData[9],
           'qc09': postData[10],   
           'qc10': postData[11],
           'qc49': postData[12],
           'qc52': postData[13],
           'qc11': postData[14],
           'qc38': postData[15],
           'qc11_1': postData[16],
           'qc220': postData[17],
           'qc220_1': postData[18],
           'qc221': postData[19],
           'qc222': postData[20],  
           'qc223': postData[21],
           'qc223_2': postData[22],
           'qc223_3': postData[23],
           'qc224': postData[24],
           'qc228': postData[25],
           'qc229': postData[26],
           'qc225': postData[27],
           'qc233': postData[28],
           'qc232': postData[29],
           'qc120': postData[30],   
           'qc227': postData[31],   
           'qc230': postData[32],
           'qc234': postDataContinues[2],
           'qc12': postDataContinues[3],
           'qc231': postDataContinues[4],
           'qc13': postDataContinues[5],
           'qc14': postDataContinues[6],
           'qc16': postDataContinues[7],
           'qc17': postDataContinues[8],
           'qc18': postDataContinues[9],
           'qc20': postDataContinues[10],  
           'qc20_1': postDataContinues[11],
           'qc20_2': postDataContinues[12],
           'qc20_3': postDataContinues[13],
           'qc62': postDataContinues[14],
           'qc51': postDataContinues[15],
           'qc24': postDataContinues[16],
           'qc25': postDataContinues[17],
           'qc27_1': postDataContinues[18],
           'qc29': postDataContinues[19],
           'qc30': postDataContinues[20],    
           'qc65': postDataContinues[21],
           'qc61': postDataContinues[22],
           'qc30': postDataContinues[23],
           'qc31': postDataContinues[24],
           'qc33': postDataContinues[25],  
           'qc34': postDataContinues[26],
           'qc63': postDataContinues[27],
           'qc50': postDataContinues[28],
           'qc39': postDataContinues[29],
           'qc40': postDataContinues[30],
           'qc41': postDataContinues[31],  
           'QC226_1': postDataContinues[36],
           'QC226_2': postDataContinues[37],
           'QC226': postDataContinues[38], 
           'company_id' : companyNameId,                                        
        }
        if models.economic.objects.filter(company_id=companyNameId):
            models.economic.objects.filter(company_id=companyNameId).update(**dict)
        else:
            models.economic.objects.create(**dict)
    return render(
        request,
        "index.html", 
        {

       }
    )    


def addPersonnel(request):
    postData = request.POST.getlist('personnelData[]')
    username = request.session.get('username','anybody')
    personnelId = request.POST.get('personnelId') 
    
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']

    if lsSuperUser is  True:  #管理员添加    
        dict = {
           'qd01': postData[2],
           'qd03': postData[3],
           'qd25': postData[4],
           'qd21': postData[5],
           'qd26': postData[6],
           'qd14': postData[7],
           'qd05': postData[8],
           'qd18': postData[11],
           'qd06': postData[12],
           'qd07': postData[13],   
           'qd08': postData[14],
           'qd09': postData[15],
           'qd30': postData[16],
           'qd31': postData[17],
           'qd32': postData[18],
           'qd33': postData[19],
           'qd34': postData[20],
           'qd35': postData[21],
           'qd36': postData[22],
           'qd27': postData[24],  
           'qd28': postData[25],   
        }        
        models.personnel.objects.filter(id=personnelId).update(**dict)
    else:
        resultUsernameId = models.userProfile.objects.values("id").filter(username=username)
        for i in resultUsernameId:
            id = str(i['id']) 
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
        for i in resultCompanyNameId:
            companyNameId = str(i['id'])   
        dict = {
           'qd01': postData[2],
           'qd03': postData[3],
           'qd25': postData[4],
           'qd21': postData[5],
           'qd26': postData[6],
           'qd14': postData[7],
           'qd05': postData[8],
           'qd18': postData[11],
           'qd06': postData[12],
           'qd07': postData[13],   
           'qd08': postData[14],
           'qd09': postData[15],
           'qd30': postData[16],
           'qd31': postData[17],
           'qd32': postData[18],
           'qd33': postData[19],
           'qd34': postData[20],
           'qd35': postData[21],
           'qd36': postData[22],
           'qd27': postData[24],  
           'qd28': postData[25],   
           'company_id' : companyNameId,                                        
        }
    
        if models.personnel.objects.filter(company_id=companyNameId):
            models.personnel.objects.filter(company_id=companyNameId).update(**dict)
        else:
            models.personnel.objects.create(**dict)
      
    return render(
        request,
        "index.html", 
        {

       }
    )    
    
def addActivities(request):
    postData = request.POST.getlist('activitiesData[]')
    postDataContinues = request.POST.getlist('activitiesContinuesData[]')  
    username = request.session.get('username','anybody') 
    activitiesId = request.POST.get('activitiesId')
    print("111111111111111111111111111111111111")
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']

    if lsSuperUser is  True:  #管理员添加   
        print("222222222222222222222222222222222222")
        dict = {
           'qj09': postData[2],
           'qj67': postData[3],
           'qj09_1': postData[4],
           'qj09_2': postData[5],
           'qj09_3': postData[6],
           'qj20': postData[8],
           'qj23_1': postData[9],
           'qj23_2': postData[10],
           'qj23_3': postData[11],
           'qj23_4': postData[12],   
           'qj23_6': postData[13],
           'qj23_7': postData[14],
           'qj33': postData[15],
           'qj33_1': postData[16],
           'qj33_2': postData[17],
           'qj33_4': postData[18],
           'qj33_3': postData[19],
           'qj23_5': postData[20],
           'qj250': postData[22],
           'qj251': postData[23],  
           'qj01': postData[25],
           'qj07_0': postData[26],
           'qj07_1': postData[27],
           'qj07_2': postData[28],
           'qj55': postData[31],
           'qj56': postData[32],
           'qj56_1': postData[33],
           'qj55_1': postData[34],
           'qj55_2': postData[35],
           'qj74': postData[36],      
           'qj57_1': postData[38],
           'qj75': postData[39],
           'qj83': postData[40],   
           'qj83_1': postData[41],   
           'qj82': postData[42],       
           'qj73': postDataContinues[2],
           'qj73_2': postDataContinues[3],
           'qj73_1': postDataContinues[4],
           'qj23': postDataContinues[5],
           'qj24': postDataContinues[6],
           'qj70': postDataContinues[8],
           'qj71': postDataContinues[9],
           'qj72': postDataContinues[10],
           'qj99': postDataContinues[12],  
           'qj90': postDataContinues[13],
           'qj92': postDataContinues[14],
           'qj102': postDataContinues[15],
           'qj25': postDataContinues[17],
           'qj79': postDataContinues[18],
           'qj77': postDataContinues[19],
           'qj79_1': postDataContinues[20],
           'qj79_2': postDataContinues[21],
           'qj85': postDataContinues[22],
           'qj85_1': postDataContinues[23],    
           'qj86': postDataContinues[24],
           'qj86_1': postDataContinues[25],
           'qj87': postDataContinues[26],
           'qj87_1': postDataContinues[27],
           'qj101': postDataContinues[28],  
           'qj101_1': postDataContinues[29],
           'qj100': postDataContinues[30],
           'qj100_1': postDataContinues[31],
           'qj98_1': postDataContinues[32],
           'qj27_1': postDataContinues[33],
           'qj28_1': postDataContinues[34],  
           'qj80_1': postDataContinues[36],
           'qj80': postDataContinues[37],
           'qj52': postDataContinues[40], 
           'qj58': postDataContinues[42],  
           'qj59': postDataContinues[43],
           'qj61': postDataContinues[44],
           'qj62': postDataContinues[45],                                    
        }  
        models.activities.objects.filter(id=activitiesId).update(**dict)        
    else:
        resultUsernameId = models.userProfile.objects.values("id").filter(username=username) #根据用户名获取用户id
        for i in resultUsernameId:
            id = str(i['id']) 
        resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id) #根据用户id获取公司id
        for i in resultCompanyNameId:
            companyNameId = str(i['id']) 
        print(companyNameId)     
        dict = {
           'qj09': postData[2],
           'qj67': postData[3],
           'qj09_1': postData[4],
           'qj09_2': postData[5],
           'qj09_3': postData[6],
           'qj20': postData[8],
           'qj23_1': postData[9],
           'qj23_2': postData[10],
           'qj23_3': postData[11],
           'qj23_4': postData[12],   
           'qj23_6': postData[13],
           'qj23_7': postData[14],
           'qj33': postData[15],
           'qj33_1': postData[16],
           'qj33_2': postData[17],
           'qj33_4': postData[18],
           'qj33_3': postData[19],
           'qj23_5': postData[20],
           'qj250': postData[22],
           'qj251': postData[23],  
           'qj01': postData[25],
           'qj07_0': postData[26],
           'qj07_1': postData[27],
           'qj07_2': postData[28],
           'qj55': postData[31],
           'qj56': postData[32],
           'qj56_1': postData[33],
           'qj55_1': postData[34],
           'qj55_2': postData[35],
           'qj74': postData[36],      
           'qj57_1': postData[38],
           'qj75': postData[39],
           'qj83': postData[40],   
           'qj83_1': postData[41],   
           'qj82': postData[42],       
           'qj73': postDataContinues[2],
           'qj73_2': postDataContinues[3],
           'qj73_1': postDataContinues[4],
           'qj23': postDataContinues[5],
           'qj24': postDataContinues[6],
           'qj70': postDataContinues[8],
           'qj71': postDataContinues[9],
           'qj72': postDataContinues[10],
           'qj99': postDataContinues[12],  
           'qj90': postDataContinues[13],
           'qj92': postDataContinues[14],
           'qj102': postDataContinues[15],
           'qj25': postDataContinues[17],
           'qj79': postDataContinues[18],
           'qj77': postDataContinues[19],
           'qj79_1': postDataContinues[20],
           'qj79_2': postDataContinues[21],
           'qj85': postDataContinues[22],
           'qj85_1': postDataContinues[23],    
           'qj86': postDataContinues[24],
           'qj86_1': postDataContinues[25],
           'qj87': postDataContinues[26],
           'qj87_1': postDataContinues[27],
           'qj101': postDataContinues[28],  
           'qj101_1': postDataContinues[29],
           'qj100': postDataContinues[30],
           'qj100_1': postDataContinues[31],
           'qj98_1': postDataContinues[32],
           'qj27_1': postDataContinues[33],
           'qj28_1': postDataContinues[34],  
           'qj80_1': postDataContinues[36],
           'qj80': postDataContinues[37],
           'qj52': postDataContinues[40], 
           'qj58': postDataContinues[42],  
           'qj59': postDataContinues[43],
           'qj61': postDataContinues[44],
           'qj62': postDataContinues[45], 
           'company_id' : companyNameId,                                      
        }
    
        if models.activities.objects.filter(company_id=companyNameId):
            models.activities.objects.filter(company_id=companyNameId).update(**dict)
        else:
            models.activities.objects.create(**dict)        
  
    return render(
        request,
        "index.html", 
        {

       }
    )      
    
    
    
def delProject(request):
    postData = request.POST
    delid = postData.get('delid')
    models.projects.objects.filter(id=delid).delete() 

      
    return render(
        request,
        "index.html", 
        {

       }
    )  

def delTmpProject(request):
    postData = request.POST
    delid = postData.get('delid')
    print(delid)
    models.projects.objects.filter(id=delid).delete() 

      
    return render(
        request,
        "index.html", 
        {

       }
    )      
    
    
    
def member(request): 
    username = request.session.get('username','anybody')
    resultId = models.userProfile.objects.values("id").filter(username=username)
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    id = ''
    for i in resultId:
        id = i['id'] 
    resultUser = models.userProfile.objects.get(username=username)  
    return render(
        request,
        "member.html", 
        {
          "resultUser":resultUser,
          "username":username,
          "superuser":superuser,
        }
    )   
    
def saveUserinfo(request):
    postData = request.POST
    #username = postData.get("username")
    username = request.session.get('username','anybody')
    id = ''
    CompanyNameId = ''

    resultUsernameId = models.userProfile.objects.values("id").filter(username=username)
    for i in resultUsernameId:
        id = str(i['id']) 

    resultCompanyNameId = models.companyInfo.objects.values("id").filter(username_id=id)
    for i in resultCompanyNameId:
        companyNameId = str(i['id'])   
        
    dictUserInfo = {
        "nickname": postData['nickname'], 
        "phone": postData['phone'], 
        "email": postData['email'], 
        "companyname": postData['companyname'],                                 
    }  
    dictCompanyInfo = {
        "companyname": postData['companyname'], 
    }

    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperuser = i['is_superuser']
        
    if str(lsSuperuser) == 'True':
        models.userProfile.objects.filter(id=id).update(**dictUserInfo)
    else:
        models.userProfile.objects.filter(id=id).update(**dictUserInfo)    
        models.companyInfo.objects.filter(id=companyNameId).update(**dictCompanyInfo)

    return render(
        request,
        "member.html", 
        {

       }
    )  
    
    
def changepasswd(request): 
    username = request.session.get('username','anybody')
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    return render(
        request,
        "changepasswd.html", 
        {
            "username":username,
            "superuser":superuser,
        }
    )    
    
    
def changePassword(request):
    username = request.session.get('username','anybody')
    postData = request.POST
    oldpassword = postData.get('oldpassword')
    password = make_password(postData.get('password'))  

    user = authenticate(username=username,password=oldpassword)
    if user is not None:       
        models.userProfile.objects.filter(username=username).update(password=password)   
    return render(
        request,
        "changepasswd.html", 
        {
          
        }
    )       
    
    

def membermanager(request):
    username = request.session.get('username','anybody')  
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)     
    return render(
        request,
        "membermanager.html", 
        {
          "username":username,
          "superuser":superuser,
        }
    )  
    
def getcompanyinfo(request):       
    sql = ''
    sql_count = ''
    ID = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')
    company = request.GET.get('company')
    print(company)
    start = str((int(p)-1) * int(l))
    end = str(l)
    if company is not None: #搜索
        sql = 'select auth_user.id,auth_user.username,auth_user.phone,auth_user.hyperlink,auth_user.is_superuser,app01_companyinfo.companyname  from auth_user,app01_companyinfo where auth_user.id = app01_companyinfo.username_id and  app01_companyinfo.companyname  like ' + "'%"  +  company  + "%' " +  ' limit '  +  start + ','  + end
        sql_count = 'select count(*)  from auth_user  where username  like ' + "'%"  +  company  + "%' " +  ' limit '  +  start + ','  + end
        print(sql)
    else: #不搜索
        sql = 'select auth_user.id,auth_user.username,auth_user.phone,auth_user.hyperlink,auth_user.is_superuser,app01_companyinfo.companyname  from auth_user,app01_companyinfo where auth_user.id = app01_companyinfo.username_id '  +  ' limit '  +  start + ','  + end
        print(sql)
        sql_count = 'select count(t.id) from  (select  auth_user.id,auth_user.username,auth_user.phone,auth_user.hyperlink,auth_user.is_superuser,app01_companyinfo.companyname  from auth_user,app01_companyinfo where auth_user.id = app01_companyinfo.username_id ) t'
    cursor = connection.cursor()
    cursor.execute(sql)
    rawData = cursor.fetchall()    
    col_names = [desc[0] for desc in cursor.description]
    result = []
    
    for row in rawData:
        objDict = {}
        
        for index, value in enumerate(row):           
            objDict[col_names[index]] = value       
    
        result.append(objDict)
    cursor.execute(sql_count)
    count = cursor.fetchall()
    count = count[0][0]      
    dict = {"code":0,"msg":"","count":count,"data":result}
    return HttpResponse(json.dumps(dict), content_type="application/json")        
 
 
def getuserinfo(request):       
    sql = ''
    sql_count = ''
    ID = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')
    username = request.GET.get('username')
    print(username)
    start = str((int(p)-1) * int(l))
    end = str(l)
    if username is not None:
        sql = 'select id,username,nickname,phone,email, companyname,hyperlink,is_superuser  from auth_user  where username  like ' + "'%"  +  username  + "%' " +  '  and   id <> 1  order by id  DESC  limit '  +  start + ','  + end  
        sql_count = 'select count(*)  from auth_user  where username  like ' + "'%"  +  username  + "%' " +  '  and   id <> 1  order by id  DESC limit '  +  start + ','  + end
    else:
        sql = 'select id,username,nickname,phone,email, companyname,hyperlink,is_superuser  from auth_user  where id <> 1   order by id  DESC  limit '  +  start + ','  + end + ''
        sql_count = 'select count(*)  from  auth_user'
    cursor = connection.cursor()
    cursor.execute(sql)
    rawData = cursor.fetchall()    
    col_names = [desc[0] for desc in cursor.description]
    result = []
    
    for row in rawData:
        objDict = {}
        
        for index, value in enumerate(row):           
            objDict[col_names[index]] = value       
    
        result.append(objDict)
    cursor.execute(sql_count)
    count = cursor.fetchall()
    count = count[0][0]      
    dict = {"code":0,"msg":"","count":count,"data":result}
    return HttpResponse(json.dumps(dict), content_type="application/json")   


def torchgather(request):
    username = request.session.get('username','anybody') 
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)      
    return render(
        request,
        "torchgather.html", 
        {
              "username":username, 
              "superuser":superuser,
        }
    )   
    
    
def getStatistics(request):
    postData = request.GET
    companyname = postData.get('companyname')

    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    companyNameId = ''
    for i in resultId:
        companyNameId = i['id']

    try:
        resultStatistics = models.statistics.objects.get(company_id=companyNameId)
        return render(
            request,
            "getstatistics.html", 
            {
              'resultStatistics':resultStatistics,
            }
        )       
    except:
        return render(
            request,
            "getstatistics.html", 
            {
              
            }
        )   
    
    
def getCompany(request):
    postData = request.GET
    companyname = postData.get('companyname')
 
    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    companyNameId = ''
    for i in resultId:
        companyNameId = i['id']
    print(companyNameId)
        
    try:    
        resultCompany = models.company.objects.get(company_id=companyNameId)
        return render(
            request,
            "getcompany.html", 
            {
              'resultCompany':resultCompany,
            }
        )
    except:
        return render(
            request,
            "getcompany.html", 
            {
              
            }
        )          
        
    
def getEconomic(request):
    postData = request.GET
    companyname = postData.get('companyname')
    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    companyNameId = ''
    for i in resultId:
        companyNameId = i['id']    
    try:    
        resultEconomic = models.economic.objects.get(company_id=companyNameId)
        return render(
            request,
            "geteconomic.html", 
            {
              'resultEconomic':resultEconomic,
            }
        )
    except:
        return render(
            request,
            "geteconomic.html", 
            {
              
            }
        )       
   
    
def getPersonnel(request):
    postData = request.GET
    companyname = postData.get('companyname')
    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    companyNameId = ''
    for i in resultId:
        companyNameId = i['id']
        
    try:    
        resultPersonnel = models.personnel.objects.get(company_id=companyNameId)
        return render(
            request,
            "getpersonnel.html", 
            {
              'resultPersonnel':resultPersonnel,
            }
        )
    except:
        return render(
            request,
            "getpersonnel.html", 
            {
              
            }
        )       
            
    
def getProjects(request):
    postData = request.GET
    companyname = postData.get('companyname')
    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    companyNameId = ''
    for i in resultId:
        companyNameId = i['id']
    print(companyNameId)    
    try:  
        resultProjects = models.projects.objects.get(company_id=companyNameId)
        return render(
            request,
            "getproject.html", 
            {   
                resultProjects:resultProjects,
            }
        ) 
    except:
        return render(
            request,
            "getproject.html", 
            {
              
            }
        )          
    
def getActivities(request):
    postData = request.GET
    companyname = postData.get('companyname')
    resultId = models.companyInfo.objects.values("id").filter(companyname=companyname)
    companyNameId = ''
    for i in resultId:
        companyNameId = i['id']
        
    try:    
        resultActivities = models.activities.objects.get(company_id=companyNameId)
        return render(
            request,
            "getactivities.html", 
            {
              'resultActivities':resultActivities,
            }
        )
    except:
        return render(
            request,
            "getactivities.html", 
            {
              
            }
        )   
        

    
    
def addUser(request):
    
    return render(
        request,
        "adduser.html", 
        {
          
        }
    )     
                                   
def saveUser(request):  #管理员增加保存用户的信息
    postData = request.POST
    username = request.session.get('username','anybody') 
    superuser = postData.get("superuser")
    id = postData.get("id") #修改用户信息用的
    print(superuser)
    if id is not None:  #获取到id就是修改用户表
        dictUser = {         
               'username' : postData.get("username"),    
               'nickname' : postData.get("nickname"), 
               'password' : make_password(postData.get("password")), 
               'phone' : postData.get("phone"), 
               'email' : postData.get("email"),
               'companyname' : postData.get("companyname"),                          
        }          
        try:   #修改管理员用户
            int(superuser) == 1
            models.userProfile.objects.filter(id=id).update(**dictUser)
        except:   #修改普通用户                            
            dictCompany = {                
                'companyname': postData.get("companyname"),
                'username_id': id
            }
            models.userProfile.objects.filter(id=id).update(**dictUser)   
            models.companyInfo.objects.filter(id=id).update(**dictUser)     #修改公司表   
    else: #没有获取到id就是新增

        dictUser = {         
           'username' : postData.get("username"),    
           'nickname' : postData.get("nickname"), 
           'password' : make_password(postData.get("password")), 
           'phone' : postData.get("phone"), 
           'email' : postData.get("email"),
           'companyname' : postData.get("companyname"),   
           'is_superuser' :postData.get("superuser"),                                        
        }  
        try:
            int(superuser) == 1  #新增管理员       
            models.userProfile.objects.create(**dictUser)
        except:
            resultId = models.userProfile.objects.values("id").filter(username=username)
            for i in resultId:
                id = i['id'] 
              
    #        resultCompanyName = models.companyInfo.objects.values("id").filter(username_id=id)
    #        for i in resultCompanyName:
    #            CompanyNameId = i['id']                
            dictCompany = {
                'companyname': postData.get("companyname"),
                'username_id': id
            }
            models.userProfile.objects.create(**dictUser)
            models.companyInfo.objects.create(**dictCompany)

    return render(
            request,
            "adduser.html", 
            {
    
            }                
        )      
    
    
    
def saveOwnUser(request):  #每个人修改自己的信息
    postData = request.POST
    username = request.session.get('username','anybody') 
    resultId = models.userProfile.objects.values('id').filter(username=username)          
    for i in resultId:  #知找到自己的id
        id = i['id']       
    superuser = models.userProfile.objects.values("is_superuser").filter(username=username)
    for i in superuser:
        lsSuperUser = i['is_superuser']        
    print(lsSuperUser)   
    print("111111111111111111111111111111")   
    if lsSuperUser is True: #管理员保存        
        
        dictUser = {         
           'username' : postData.get("username"),    
           'nickname' : postData.get("nickname"), 
           'password' : make_password(postData.get("password")), 
           'phone' : postData.get("phone"), 
           'email' : postData.get("email"),
           'companyname' : postData.get("companyname"),                          
        }  
        print("2222222222222222222222222222")  
        models.companyInfo.objects.filter(username_id=id).update(**dictUser)

    else:               #普通用户保存
        resultCompanyId = models.companyInfo.objects.values("id").filter(username_id=id)  #找到公司id
        for i in resultCompanyId:
          companyNameId = i['id']
        dictCompany = {
            'companyname' : postData.get("companyname"),
            'username_id' :   id,         
        }
        dictUser = {         
           'username' : postData.get("username"),    
           'nickname' : postData.get("nickname"), 
           'password' : make_password(postData.get("password")), 
           'phone' : postData.get("phone"), 
           'email' : postData.get("email"),
           'companyname' : postData.get("companyname"),                          
        }          
           
        models.userProfile.objects.filter(id=id).update(**dictUser)        
        models.companyInfo.objects.filter(id=companyNameId).update(**dictCompany)

    return render(
            request,
            "adduser.html", 
            {
    
            }                
        )  
    
    
    
    
    
    
    
    
    
    
    
    
    
def editUser(request):
    getData = request.GET
    id = getData.get("id")    
    result = models.userProfile.objects.get(id=id)
    return render(
            request,
            "edituser.html", 
            {               
                'result' : result,
            }                
    )          
    
def delUser(request):
    postData = request.POST
    delid = postData.get('delid')
    models.userProfile.objects.filter(id=delid).delete() 

      
    return render(
        request,
        "membermanager.html", 
        {

       }
    )  
    
def delCompany(request):
    postData = request.POST
    companyname = postData.get('delcompanyname')    
    print(companyname)
    return render(
        request,
        "torchgather.html", 
        {

       }
    )  





    
def createExcel(request):
    postData = request.POST
    companyName = postData.get('companyname')

    resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyName)
    for i in resultCompanyNameId:
        companyNameId = str(i['id'])
                
    workbook = load_workbook('E:\\1.xlsx')
    workbook.active = 0
    workbook1 = workbook.active
    print("1111111111111111111111111111111111")
    resulstatisticst = models.statistics.objects.values().filter(company_id=companyNameId)
    print("22222222222222222222222222222222222") 
    for item in resulstatisticst:
        workbook1['F2'] = item['organizationCode']
        workbook1['L2'] = item['areaNumber']
        workbook1['D3'] = item['enterpriseName']
        workbook1['K3'] = item['natureOfCorporation']
        workbook1['D4'] = item['corporateGender'] 
        workbook1['G4'] = item['birthday']
        workbook1['J4'] = item['education']
        workbook1['D5'] = item['address']
        workbook1['L5'] = item['postalCode']
        workbook1['D6'] = item['registeredAddress']  
        workbook1['D7'] = item['manager']
        workbook1['G7'] = item['telephone']
        workbook1['K7'] = item['fax']
        workbook1['D8'] = item['statisticalControlOfficer']
        workbook1['G8'] = item['preparedBy']  
        workbook1['J8'] = item['preparedByTelephone']
        workbook1['C9'] = item['fillingTime']
        workbook1['F9'] = item['email']
        workbook1['C10'] = item['url']
        workbook1['K10'] = item['preparedByMobilephone'] 
        
    print("3333333333333333333333333333333333333333333") 
           
    resultcompany = models.company.objects.values().filter(company_id=companyNameId) 
    workbook.active = 1
    workbook1 = workbook.active    
    for item in resultcompany:
        workbook1['C3'] = item['qb07_2']
        workbook1['C4'] = item['qb07_3']
        workbook1['C5'] = item['qb08']
        workbook1['C6'] = item['qb21']
        workbook1['C7'] = item['qb22'] 
        workbook1['C8'] = item['qb101']
        workbook1['C9'] = item['qb03_0']
        workbook1['C10'] = item['qb03_1']
        workbook1['C11'] = item['qb04']
        workbook1['C12'] = item['qb04_0']  
        workbook1['C13'] = item['qb20_1']
        workbook1['C14'] = item['qb20']
        workbook1['C15'] = item['qb06']
        workbook1['C17'] = item['qb06_1']
        workbook1['C18'] = item['qb06_2']    
        workbook1['C19'] = item['qb18']
        workbook1['C20'] = item['qb09']
        workbook1['C21'] = item['qb10']
        workbook1['C22'] = item['qb11']  
        workbook1['C23'] = item['qb13']
        workbook1['C24'] = item['qb12']
        workbook1['C25'] = item['qb14']
        workbook1['C26'] = item['qb14_1']
        workbook1['C27'] = item['qb14_2']    
        workbook1['C28'] = item['qb15']    
        workbook1['C29'] = item['qb15_1']
        workbook1['C30'] = item['qb15_2']
        workbook1['C31'] = item['qb15_3']
        workbook1['C32'] = item['qb15_4']  
        workbook1['C33'] = item['qb15_5']
        workbook1['C34'] = item['qb16']
        workbook1['C35'] = item['qb16_1']                        
    
    resulteconomic = models.economic.objects.values().filter(company_id=companyNameId)
    workbook.active = 2
    workbook1 = workbook.active      
    for item in resulteconomic:
        workbook1['D3'] = item['qc02']
        workbook1['D4'] = item['qc02_05']
        workbook1['D5'] = item['qc55']
        workbook1['D6'] = item['qc06']
        workbook1['D7'] = item['qc06_1'] 
        workbook1['D8'] = item['qc06_2']
        workbook1['D9'] = item['qc06_3']
        workbook1['D10'] = item['qc06_4']
        workbook1['D11'] = item['qc07']
        workbook1['D12'] = item['qc09']  
        workbook1['D13'] = item['qc10']
        workbook1['D14'] = item['qc49']
        workbook1['D15'] = item['qc52']
        workbook1['D16'] = item['qc11']        
        workbook1['D17'] = item['qc38']    
        workbook1['D18'] = item['qc11_1']
        workbook1['D19'] = item['qc220']
        workbook1['D20'] = item['qc220_1']
        workbook1['D21'] = item['qc221']  
        workbook1['D22'] = item['qc222']
        workbook1['D23'] = item['qc223']
        workbook1['D24'] = item['qc223_2']
        workbook1['D25'] = item['qc223_3']
        workbook1['D26'] = item['qc224']    
        workbook1['D27'] = item['qc228']    
        workbook1['D28'] = item['qc229']
        workbook1['D29'] = item['qc225']
        workbook1['D30'] = item['qc233']
        workbook1['D31'] = item['qc232']  
        workbook1['D32'] = item['qc120']
        workbook1['D33'] = item['qc227']
        workbook1['D34'] = item['qc230'] 
        workbook1['D38'] = item['qc234'] 
        workbook1['D39'] = item['qc12']   
        workbook1['D40'] = item['qc231']
        workbook1['D41'] = item['qc13']  
        workbook1['D42'] = item['qc14']
        workbook1['D43'] = item['qc16']
        workbook1['D44'] = item['qc17']
        workbook1['D45'] = item['qc18']        
        workbook1['D46'] = item['qc20']
        workbook1['D47'] = item['qc20_1']    
        workbook1['D48'] = item['qc20_2']
        workbook1['D49'] = item['qc20_3']
        workbook1['D50'] = item['qc62']
        workbook1['D51'] = item['qc51']  
        workbook1['D52'] = item['qc24']
        workbook1['D53'] = item['qc25']
        workbook1['D54'] = item['qc27_1']
        workbook1['D55'] = item['qc29']
        workbook1['D56'] = item['qc30']    
        workbook1['D57'] = item['qc65']    
        workbook1['D58'] = item['qc61']
        workbook1['D59'] = item['qc30']   
        workbook1['D60'] = item['qc31']
        workbook1['D61'] = item['qc33']  
        workbook1['D62'] = item['qc34']
        workbook1['D63'] = item['qc63']
        workbook1['D64'] = item['qc50']
        workbook1['D65'] = item['qc39']
        workbook1['D66'] = item['qc40']                            
        workbook1['D67'] = item['qc41']
        workbook1['B69'] = item['QC226_1']
        workbook1['B70'] = item['QC226_2'] 
        workbook1['B71'] = item['QC226']           
            
    resultpersonnel = models.personnel.objects.values().filter(company_id=companyNameId)
    workbook.active = 3
    workbook1 = workbook.active      
    for item in resultpersonnel:
        workbook1['D4'] = item['qd01']
        workbook1['D5'] = item['qd03']
        workbook1['D6'] = item['qd25']
        workbook1['D7'] = item['qd21'] 
        workbook1['D8'] = item['qd26']
        workbook1['D9'] = item['qd14']
        workbook1['D10'] = item['qd05']      
        workbook1['D13'] = item['qd18']
        workbook1['D14'] = item['qd06']
        workbook1['D15'] = item['qd07']
        workbook1['D16'] = item['qd08']        
        workbook1['D17'] = item['qd09']
        workbook1['D18'] = item['qd30']    
        workbook1['D19'] = item['qd31']
        workbook1['D20'] = item['qd32']
        workbook1['D21'] = item['qd33']
        workbook1['D22'] = item['qd34']  
        workbook1['D23'] = item['qd35']
        workbook1['D24'] = item['qd36']
        workbook1['D26'] = item['qd27']
        workbook1['D27'] = item['qd28']    
     
          
    resultprojects = models.projects.objects.values().filter(company_id=companyNameId)
    count = models.projects.objects.values().filter(company_id=companyNameId).count()

    workbook.active = 4
    workbook1 = workbook.active 
    for i in range(count):
        i = str(i+3)       
        for item in resultprojects:
            
            workbook1[str("B"+i)] = item['projectName']   
            workbook1[str("C"+i)] = item['projectFrom']
            workbook1[str("D"+i)] = item['developmentForm']
            workbook1[str("E"+i)] = item['achievement']
            workbook1[str("F"+i)] = item['economicGoals'] 
            workbook1[str("G"+i)] = item['activityType']
            workbook1[str("H"+i)] = item['startTime']
            workbook1[str("I"+i)] = item['endTime']
            workbook1[str("J"+i)] = item['personnel']
            workbook1[str("K"+i)] = item['time']  
            workbook1[str("L"+i)] = item['stage']
            workbook1[str("M"+i)] = item['funds']
            workbook1[str("N"+i)] = item['capital']                      
            
    
       
    resultactivities = models.activities.objects.values().filter(company_id=companyNameId)  
    workbook.active = 5
    workbook1 = workbook.active      
    for item in resultactivities:
        workbook1['D4'] = item['qj09']
        workbook1['D5'] = item['qj67']
        workbook1['D6'] = item['qj09_1']
        workbook1['D7'] = item['qj09_2'] 
        workbook1['D8'] = item['qj09_3']
        
        workbook1['D10'] = item['qj20']
        workbook1['D11'] = item['qj23_1']
        workbook1['D12'] = item['qj23_2']  
        workbook1['D13'] = item['qj23_3']
        workbook1['D14'] = item['qj23_4']
        workbook1['D15'] = item['qj23_6']
        workbook1['D16'] = item['qj23_7']        
        workbook1['D17'] = item['qj33']    
        workbook1['D18'] = item['qj33_1']
        workbook1['D19'] = item['qj33_2']
        workbook1['D20'] = item['qj33_4']
        workbook1['D21'] = item['qj33_3']  
        workbook1['D22'] = item['qj23_5']
        
        
        workbook1['D24'] = item['qj250']
        workbook1['D25'] = item['qj251']
        
           
        workbook1['D27'] = item['qj01']    
        workbook1['D28'] = item['qj07_0']
        workbook1['D29'] = item['qj07_1']
        workbook1['D30'] = item['qj07_2']
        workbook1['D31'] = item['qj14_1']
          
        workbook1['D34'] = item['qj55'] 
        workbook1['D35'] = item['qj56'] 
        workbook1['D36'] = item['qj56_1']   
        workbook1['D37'] = item['qj55_1']
        workbook1['D38'] = item['qj55_2']  
        workbook1['D39'] = item['qj74']
        workbook1['D40'] = item['qj57']
        workbook1['D41'] = item['qj57_1']
        workbook1['D42'] = item['qj75']   
        workbook1['D43'] = item['qj83']
        workbook1['D44'] = item['qj83_1']
        workbook1['D45'] = item['qj82'] 
        
        workbook1['D49'] = item['qj73']
        workbook1['D50'] = item['qj73_2']   
        workbook1['D51'] = item['qj73_1']
        workbook1['D52'] = item['qj23']
        workbook1['D53'] = item['qj24']    
        
        workbook1['D55'] = item['qj70']
        workbook1['D56'] = item['qj71']
        workbook1['D57'] = item['qj72'] 
        
        workbook1['D59'] = item['qj57_1']
        workbook1['D60'] = item['qj75']   
        workbook1['D61'] = item['qj83']
        workbook1['D62'] = item['qj83_1'] 

        workbook1['D64'] = item['qj25'] 
        workbook1['D65'] = item['qj79'] 
        workbook1['D66'] = item['qj77']   
        workbook1['D67'] = item['qj79_1']
        workbook1['D68'] = item['qj79_2']  
        workbook1['D69'] = item['qj85']
        workbook1['D70'] = item['qj85_1']
        workbook1['D71'] = item['qj86']
        workbook1['D72'] = item['qj86_1']   
        workbook1['D73'] = item['qj87']
        workbook1['D74'] = item['qj87_1']
        workbook1['D75'] = item['qj101']   
        workbook1['D76'] = item['qj101_1']
        workbook1['D77'] = item['qj100']  
        workbook1['D78'] = item['qj100_1']
        workbook1['D79'] = item['qj98_1']
        workbook1['D80'] = item['qj27_1']
        workbook1['D81'] = item['qj28_1']   
        
        
        workbook1['D83'] = item['qj80_1']
        workbook1['D84'] = item['qj80']
        
        workbook1['D87'] = item['qj52']  
        
        workbook1['D89'] = item['qj58']
        workbook1['D90'] = item['qj59']
        workbook1['D91'] = item['qj61']
        workbook1['D92'] = item['qj62']                                                
      
        
        
                   
           
        
                                           
    timestr=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filepath= BASE_DIR + '''\static\dexi-''' + timestr + ".xlsx"                           
    filename = 'dexi-' + timestr + '.xlsx'

    
  
    workbook.save(filepath) 
    dict = {
    "filename": filename , 
    }
    return HttpResponse(json.dumps(dict), content_type="application/json")



def addAll(request):
    postDataStatistics = request.POST.getlist('statisticsData[]')
    postDataStatisticsContinues  =  request.POST.getlist('statisticsContinuesData[]')
    postDataCompany = request.POST.getlist('companyData[]')   
    postDataEconomic = request.POST.getlist('economicData[]')
    postDataEconomicContinues = request.POST.getlist('economicContinuesData[]')  
    postDataPersonnel = request.POST.getlist('personnelData[]')
    postDataActivities = request.POST.getlist('activitiesData[]')   
    postDataActivitiesContinues = request.POST.getlist('activitiesContinuesData[]')    

    companyname = postDataStatistics[0]
    print(companyname)
    
        
    resultCompanyNameId = models.companyInfo.objects.values("id").filter(companyname=companyname)  #获取公司的id
    for i in resultCompanyNameId:
        companyNameId = str(i['id'])  
    
    dictStatistics = {
        'organizationCode':postDataStatistics[1],
        'areaNumber':postDataStatistics[2],
        'enterpriseName':postDataStatistics[3],
        'natureOfCorporation':postDataStatistics[4],
        'corporateGender':postDataStatistics[5],
        'birthday':postDataStatistics[6], 
        'education':postDataStatistics[7],
        'address':postDataStatistics[8],
        'postalCode':postDataStatistics[9],
        'registeredAddress':postDataStatistics[10],
        'manager':postDataStatistics[11],
        'telephone':postDataStatistics[12], 
        'fax':postDataStatistics[13],
        'statisticalControlOfficer':postDataStatistics[14],
        'preparedBy':postDataStatistics[15],
        'preparedByTelephone':postDataStatistics[16],
        'fillingTime':postDataStatistics[17],
        'email':postDataStatistics[18], 
        'url':postDataStatisticsContinues[0],
        'preparedByMobilephone':postDataStatisticsContinues[1],
        'company_id':companyNameId,
    }

           
    dictCompany = {   
        'qb07_2':postDataCompany[1],
        'qb07_3':postDataCompany[2],
        'qb08':postDataCompany[3],
        'qb21':postDataCompany[4], 
        'qb22':postDataCompany[5],
        'qb101':postDataCompany[6],
        'qb03_0':postDataCompany[7],
        'qb03_1':postDataCompany[8],
        'qb04':postDataCompany[9],
        'qb04_0':postDataCompany[10],  
        'qb20_1':postDataCompany[11],
        'qb20':postDataCompany[12],
        'qb06':postDataCompany[13],
        'qb06_1':postDataCompany[15],
        'qb06_2':postDataCompany[16],
        'qb18':postDataCompany[17], 
        'qb09':postDataCompany[18],
        'qb10':postDataCompany[19],
        'qb12':postDataCompany[20],
        'qb14':postDataCompany[21], 
        'qb14_1':postDataCompany[22],
        'qb14_2':postDataCompany[23],
        'qb15':postDataCompany[24],
        'qb15_1':postDataCompany[25],
        'qb15_2':postDataCompany[26],
        'qb15_3':postDataCompany[27], 
        'qb15_4':postDataCompany[28],
        'qb15_5':postDataCompany[29],
        'qb16':postDataCompany[30],
        'qb16_1':postDataCompany[31],
        'company_id':companyNameId,        
    }
 
    
    dictEconomic = {
        
        'qc02':postDataEconomic[1],
        'qc02_05':postDataEconomic[2], 
        'qc55':postDataEconomic[3],
        'qc06':postDataEconomic[4],
        'qc06_1':postDataEconomic[5],
        'qc06_2':postDataEconomic[6],
        'qc06_3':postDataEconomic[7],
        'qc06_4':postDataEconomic[8],
        'qc07':postDataEconomic[9],
        'qc09':postDataEconomic[10],
        'qc10':postDataEconomic[11],
        'qc49':postDataEconomic[12],
        'qc52':postDataEconomic[13],
        'qc11':postDataEconomic[14], 
        'qc38':postDataEconomic[15],
        'qc11_1':postDataEconomic[16],
        'qc220':postDataEconomic[17],
        'qc220_1':postDataEconomic[18],
        'qc221':postDataEconomic[19],
        'qc222':postDataEconomic[20], 
        'qc223':postDataEconomic[21],
        'qc223_2':postDataEconomic[22],
        'qc223_3':postDataEconomic[23],
        'qc224':postDataEconomic[24],
        'qc228':postDataEconomic[25],
        'qc229':postDataEconomic[26], 
        'qc225':postDataEconomic[27],
        'qc233':postDataEconomic[28],
        'qc232':postDataEconomic[29],
        'qc120':postDataEconomic[30],
        'qc227':postDataEconomic[31],
        'qc230':postDataEconomic[32], 
        'qc234':postDataEconomicContinues[2],
        'qc12':postDataEconomicContinues[3],
        'qc231':postDataEconomicContinues[4],
        'qc13':postDataEconomicContinues[5],
        'qc14':postDataEconomicContinues[6],
        'qc16':postDataEconomicContinues[7],
        'qc17':postDataEconomicContinues[8],
        'qc18':postDataEconomicContinues[9],
        'qc20':postDataEconomicContinues[10],
        'qc20_1':postDataEconomicContinues[11],
        'qc20_2':postDataEconomicContinues[12],
        'qc20_3':postDataEconomicContinues[13], 
        'qc62':postDataEconomicContinues[14],
        'qc51':postDataEconomicContinues[15],
        'qc24':postDataEconomicContinues[16],
        'qc25':postDataEconomicContinues[17],
        'qc27_1':postDataEconomicContinues[18],
        'qc29':postDataEconomicContinues[19], 
        'qc30':postDataEconomicContinues[20],
        'qc65':postDataEconomicContinues[21],
        'qc61':postDataEconomicContinues[22],
        'qc30':postDataEconomicContinues[23],
        'qc31':postDataEconomicContinues[24],
        'qc33':postDataEconomicContinues[25], 
        'qc34':postDataEconomicContinues[26],
        'qc63':postDataEconomicContinues[27],
        'qc50':postDataEconomicContinues[28],
        'qc39':postDataEconomicContinues[29],
        'qc40':postDataEconomicContinues[30],
        'qc41':postDataEconomicContinues[31], 
        'QC226_1':postDataEconomicContinues[32],
        'QC226_2':postDataEconomicContinues[33],
        'QC226':postDataEconomicContinues[34],
        'company_id':companyNameId,        
    }
     
    dictPersonnel = {    
        'qd01':postDataPersonnel[2],
        'qd03':postDataPersonnel[3],
        'qd25':postDataPersonnel[4],
        'qd21':postDataPersonnel[5],
        'qd26':postDataPersonnel[6],
        'qd14':postDataPersonnel[7],
        'qd05':postDataPersonnel[8],
        'qd18':postDataPersonnel[11],
        'qd06':postDataPersonnel[12], 
        'qd07':postDataPersonnel[13],
        'qd08':postDataPersonnel[14],
        'qd09':postDataPersonnel[15],
        'qd30':postDataPersonnel[16],
        'qd31':postDataPersonnel[17],
        'qd32':postDataPersonnel[18], 
        'qd33':postDataPersonnel[19],
        'qd34':postDataPersonnel[20],
        'qd35':postDataPersonnel[21],
        'qd36':postDataPersonnel[22],
        'qd27':postDataPersonnel[24],
        'qd28':postDataPersonnel[25], 
        'company_id':companyNameId,
                
    }
    print("777777777777777777777777777777777777") #这张表要全部填写
      
   
    
    
    
    dictActivities = {    
        'qj09':postDataActivities[2],
        'qj67':postDataActivities[3],
        'qj09_1':postDataActivities[4],
        'qj09_2':postDataActivities[5],
        'qj09_3':postDataActivities[6],
        'qj20':postDataActivities[8], 
        'qj23_1':postDataActivities[9],
        'qj23_2':postDataActivities[10],
        'qj23_3':postDataActivities[11],
        'qj23_4':postDataActivities[12],
        'qj23_6':postDataActivities[13],
        'qj23_7':postDataActivities[14], 
        'qj33':postDataActivities[15],
        'qj33_1':postDataActivities[16], 
        'qj33_2':postDataActivities[17],
        'qj33_4':postDataActivities[18],
        'qj33_3':postDataActivities[19],
        'qj23_5':postDataActivities[20],
        'qj250':postDataActivities[22],
        'qj251':postDataActivities[23],
        'qj01':postDataActivities[25],
        'qj07_0':postDataActivities[26],
        'qj07_1':postDataActivities[27],
        'qj07_2':postDataActivities[28],
        'qj55':postDataActivities[31], 
        'qj56':postDataActivities[32],
        'qj56_1':postDataActivities[33],
        'qj55_1':postDataActivities[34],
        'qj55_2':postDataActivities[35],
        'qj74':postDataActivities[36],
        'qj57':postDataActivities[37], 
        'qj57_1':postDataActivities[38],
        'qj75':postDataActivities[39],
        'qj83':postDataActivities[40],
        'qj83_1':postDataActivities[41],           
        'qj82':postDataActivities[42],
        
        
        
        'qj73':postDataActivitiesContinues[2], 
        'qj73_2':postDataActivitiesContinues[3],
        'qj73_1':postDataActivitiesContinues[4],
        'qj23':postDataActivitiesContinues[5],
        'qj24':postDataActivitiesContinues[6],
        'qj70':postDataActivitiesContinues[8],
        'qj71':postDataActivitiesContinues[9], 
        'qj72':postDataActivitiesContinues[10],
        'qj99':postDataActivitiesContinues[12],
        'qj90':postDataActivitiesContinues[13],
        'qj92':postDataActivitiesContinues[14],
        'qj102':postDataActivitiesContinues[15],
        'qj25':postDataActivitiesContinues[17],
        'qj79':postDataActivitiesContinues[18],
        'qj77':postDataActivitiesContinues[19],
        'qj79_1':postDataActivitiesContinues[20],
        'qj79_2':postDataActivitiesContinues[21],
        'qj85':postDataActivitiesContinues[22],
        'qj85_1':postDataActivitiesContinues[23], 
        'qj86':postDataActivitiesContinues[24],
        'qj86_1':postDataActivitiesContinues[25],
        'qj87':postDataActivitiesContinues[26],
        'qj87_1':postDataActivitiesContinues[27],
        'qj101':postDataActivitiesContinues[28],
        'qj101_1':postDataActivitiesContinues[29], 
        'qj100':postDataActivitiesContinues[30],
        'qj100_1':postDataActivitiesContinues[31],
        'qj98_1':postDataActivitiesContinues[32],
        'qj27_1':postDataActivitiesContinues[33],
        'qj28_1':postDataActivitiesContinues[34],
        'qj80_1':postDataActivitiesContinues[36], 
        'qj80':postDataActivitiesContinues[37],
        'qj52':postDataActivitiesContinues[40],
        'qj58':postDataActivitiesContinues[42],
        'qj59':postDataActivitiesContinues[43],
        'qj61':postDataActivitiesContinues[44],
        'qj62':postDataActivitiesContinues[45],     
        'company_id':companyNameId,         
    }     
    
    if len(companyname) == 0:   #没有输公司名字
       
        models.projectstmp.objects.create(**dict)      #让程序报错         
    elif models.companyInfo.objects.filter(companyname=companyname):  #该公司已经登记过
#        models.projectstmp.objects.create(**dict)      
            
        if models.statistics.objects.filter(company_id=companyNameId):
            models.statistics.objects.filter(company_id=companyNameId).update(**dictStatistics)
        else:
            models.statistics.objects.create(**dictStatistics)         
        if models.company.objects.filter(company_id=companyNameId):         
            models.company.objects.filter(company_id=companyNameId).update(**dictCompany)
        else:
            models.company.objects.create(**dictCompany)  
                        
        if models.economic.objects.filter(company_id=companyNameId):
            models.economic.objects.filter(company_id=companyNameId).update(**dictEconomic)
        else:
            models.economic.objects.create(**dictEconomic)
            
        if models.personnel.objects.filter(company_id=companyNameId):
            models.personnel.objects.filter(company_id=companyNameId).update(**dictPersonnel)
        else:
            models.personnel.objects.create(**dictPersonnel)     
        if models.activities.objects.filter(company_id=companyNameId):
            models.activities.objects.filter(company_id=companyNameId).update(**dictActivities) 
        else:
            models.activities.objects.create(**dictActivities)                                
    else:
        
        username = request.session.get('username','anybody')
        resultId = models.userProfile.objects.values("id").filter(username=username)  #获取用户的id
        for i in resultId:
            id = str(i['id'])           
        dict = {
            'username_id': id,
            'companyname': companyname,
            }

        models.companyInfo.objects.create(**dict)
        models.statistics.objects.create(**dict)
        models.company.objects.create(**dict)   
        models.economic.objects.create(**dict)  
        models.personnel.objects.create(**dict)  
        models.activities.objects.create(**dict)         

    

    return render(
        request,
        "index.html", 
        {
    
        }
    )     

        