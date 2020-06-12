from django.shortcuts import render
from anaconda_navigator.utils.py3compat import request
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from app01 import models
from _cffi_backend import string
from django.db import connection
import json
from builtins import dict
from _ast import Dict
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.utils.encoding import repercent_broken_unicode
from django.contrib.auth.hashers import make_password

# Create your views here.

#登入页面验证
def login(request,*args,**kwargs):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        postData = request.POST
        username = postData.get('username')
        password = postData.get('password')
        
        user = authenticate(username=username,password=password)
        if user is not None:
            
            request.session['username'] = username
            return HttpResponseRedirect (
            "/index/", 
           { 
               
           }      
        )
        else:
            return HttpResponseRedirect('/login/',{})
    
    
#获取index页面所有数据   
def index(request,*args,**kwargs):
    username = request.session.get('username','anybody')
    resultId = models.userProfile.objects.values("id").filter(username=username)
    id = ''
    for i in resultId:
        id = i['id']
    resultStatistics = models.statistics.objects.get(username_id=id)
    resultCompany = models.company.objects.get(username_id=id)
    resultEconomic = models.economic.objects.get(username_id=id)
    resultPersonnel = models.personnel.objects.get(username_id=id)
    resultActivities = models.activities.objects.get(username_id=id)

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
       }
    )
    
#获取项目表格数据
def getPojectList(request):
    sql = ''
    sql_count = ''
    ID = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')
    start = str((int(p)-1) * int(l))
    end = str(l)
    ID = '1'
    
    sql = 'select id,username_id,projectName,projectFrom,developmentForm,achievement,economicGoals,activityType,date_format(startTime,"%Y-%m-%d %T") as startTime,date_format(endTime,"%Y-%m-%d %T") as endTime,personnel,time,stage,funds,capital  from app01_projects  where  username_id = ' +   ID   +  ' limit '  +  start + ','  + end
    sql_count = 'select count(*)  from  app01_projects'
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



def addStatistics(request):
    postData = request.POST
    username = request.session.get('username','anybody') 
    dict = {
        'organizationCode' : postData.get('organizationCode'),
        'areaNumber' : postData.get('areaNumber'),
        'enterpriseName' : postData.get('enterpriseName'),
        'natureOfCorporation' : postData.get('natureOfCorporation'),
#        'corporateGenderId' : postData.get('corporateGenderId'),
        'birthday' : postData.get('birthday'),
#        'educationId' : postData.get('educationId'),
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
        'username_id' : '1',    
    }  
    
    models.statistics.objects.create(**dict)       
    
    return render(
        request,
        "index.html", 
        {

        }                
    )
    

    
def addProject(request):
    postData = request.POST
    username = request.session.get('username','anybody') 
    
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
        'username_id' : '1',   
    }

    models.projects.objects.create(**dict)   
     
    return render(
        request,
        "index.html", 
        {

        }                
    )
       
def addCompany(request):
    postData = request.POST.getlist('companyData[]')
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
       'qb06_1': postData[14],
       'qb06_2': postData[15],
       'qb18': postData[16],
       'qb09': postData[17],
       'qb10': postData[18],
       'qb12': postData[19],
       'qb14': postData[20],  
       'qb14_1': postData[21],
       'qb14_2': postData[22],
       'qb15': postData[23],
       'qb15_1': postData[24],
       'qb15_2': postData[25],
       'qb15_3': postData[26],
       'qb15_4': postData[27],
       'qb15_5': postData[28],
       'qb16': postData[29],
       'qb16_1': postData[30],                   
    }
        
    models.company.objects.create(**dict)   
    return render(
        request,
        "index.html", 
        {

       }
    )
    
  
def addEconomic(request):
    postData = request.POST.getlist('economicData[]')
    postDataContinues = request.POST.getlist('economicContinuesData[]') 

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
 
    models.economic.objects.create(**dict) 
      
    return render(
        request,
        "index.html", 
        {

       }
    )    


def addPersonnel(request):
    postData = request.POST.getlist('personnelData[]')
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

        
#    models.personnel.objects.create(**dict) 

      
    return render(
        request,
        "index.html", 
        {

       }
    )    
    
def addActivities(request):
    postData = request.POST.getlist('activitiesData[]')
    postDataContinues = request.POST.getlist('activitiesContinuesData[]')  
  
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
       'qj70': postDataContinues[7],
       'qj71': postDataContinues[8],
       'qj72': postDataContinues[9],
       'qj99': postDataContinues[10],  
       'qj90': postDataContinues[11],
       'qj92': postDataContinues[12],
       'qj102': postDataContinues[13],
       'qj25': postDataContinues[14],
       'qj79': postDataContinues[15],
       'qj77': postDataContinues[16],
       'qj79_1': postDataContinues[17],
       'qj79_2': postDataContinues[18],
       'qj85': postDataContinues[19],
       'qj85_1': postDataContinues[20],    
       'qj86': postDataContinues[21],
       'qj86_1': postDataContinues[22],
       'qj87': postDataContinues[23],
       'qj87_1': postDataContinues[24],
       'qj101': postDataContinues[25],  
       'qj101_1': postDataContinues[26],
       'qj100': postDataContinues[27],
       'qj100_1': postDataContinues[28],
       'qj98_1': postDataContinues[29],
       'qj27_1': postDataContinues[30],
       'qj28_1': postDataContinues[31],  
       'qj80_1': postDataContinues[36],
       'qj80': postDataContinues[37],
       'qj52': postDataContinues[38], 
       'qj58': postDataContinues[31],  
       'qj59': postDataContinues[36],
       'qj61': postDataContinues[37],
       'qj62': postDataContinues[38],                                       
    }

        
#    models.personnel.objects.create(**dict) 

      
    return render(
        request,
        "index.html", 
        {

       }
    )      
    
    
    
def delProject(request):
    postData = request.POST.get('delid')

        
#    models.personnel.objects.create(**dict) 

      
    return render(
        request,
        "index.html", 
        {

       }
    )  
    
    
def member(request): 
    username = request.session.get('username','anybody')
    resultId = models.userProfile.objects.values("id").filter(username=username)
    id = ''
    for i in resultId:
        id = i['id'] 
    resultUser = models.userProfile.objects.get(username=username)  
    return render(
        request,
        "member.html", 
        {
          "resultUser":resultUser,
        }
    )   
    
def saveUserinfo(request):
    postData = request.POST
    username = postData.get("username")
    dict = {
        "nickname": postData['nickname'], 
        "phone": postData['phone'], 
        "email": postData['email'], 
        "companyname": postData['companyname'],                                 
    }  
    models.userProfile.objects.filter(username=username).update(**dict)
    return render(
        request,
        "member.html", 
        {

       }
    )  
    
    
def changepasswd(request): 
    username = request.session.get('username','anybody')
    return render(
        request,
        "changepasswd.html", 
        {
  
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
    return render(
        request,
        "membermanager.html", 
        {
          
        }
    )   
 
 
def getuserinfo(request):       
    sql = ''
    sql_count = ''
    ID = ''
    getData = request.GET
    p = request.GET.get('page')
    l = request.GET.get('limit')
    start = str((int(p)-1) * int(l))
    end = str(l)
    ID = '1'
    
    sql = 'select username,nickname,phone,email, companyname,hyperlink  from auth_user '  +  ' limit '  +  start + ','  + end
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
    return render(
        request,
        "torchgather.html", 
        {
          
        }
    )   
    
    
def getStatistics(request):
    postData = request.GET
    username = postData.get('username')
 
    resultId = models.userProfile.objects.values("id").filter(username=username)
    resultStatistics = models.statistics.objects.get(username_id=resultId)
    return render(
        request,
        "getstatistics.html", 
        {
          'resultStatistics':resultStatistics,
        }
    )   
    
    
def getCompany(request):
    postData = request.GET
    username = postData.get('username')
 
    resultId = models.userProfile.objects.values("id").filter(username=username)
    resultCompany = models.company.objects.get(username_id=resultId)
    return render(
        request,
        "getcompany.html", 
        {
          'resultCompany':resultCompany,
        }
    )
    
def getEconomic(request):
    postData = request.GET
    username = postData.get('username')
    resultId = models.userProfile.objects.values("id").filter(username=username)
    resultEconomic = models.economic.objects.get(username_id=resultId)

    return render(
        request,
        "geteconomic.html", 
        {
          'resultEconomic':resultEconomic,
        }
    )      
    
def getPersonnel(request):
    postData = request.GET
    username = postData.get('username')
    resultId = models.userProfile.objects.values("id").filter(username=username)
    resultPersonnel = models.personnel.objects.get(username_id=resultId)
    return render(
        request,
        "getpersonnel.html", 
        {
          'resultPersonnel':resultPersonnel,
        }
    )      
    
def getProjects(request):
    postData = request.GET
    username = postData.get('username')
    print("123")
    return render(
        request,
        "getproject.html", 
        {
          
        }
    )  
    
def getActivities(request):
    postData = request.GET
    username = postData.get('username')
 
    resultId = models.userProfile.objects.values("id").filter(username=username)
    resultActivities = models.activities.objects.get(username_id=resultId)
    return render(
        request,
        "getactivities.html", 
        {
          'resultActivities':resultActivities,
        }
    )                            
        