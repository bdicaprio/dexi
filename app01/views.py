from django.shortcuts import render
from anaconda_navigator.utils.py3compat import request
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from app01 import models
from _cffi_backend import string
from django.db import connection
import json
from builtins import dict

# Create your views here.
def index(request,*args,**kwargs):
    #account = request.session.get('username','anybody')
    #result = models.technologyProjects.objects.filter(account)  
    #username_id = str("1")
    
    result = models.statistics.objects.values("username_id").filter(username_id=1)
    id_tmp = {}
    for i in result:
        id_tmp.update(i)
    
    username_id = ''  
    for value in id_tmp.values():
        username_id = value
    return render(
        request,
        "index.html", 
        {
        "result":result,  
        "username_id":username_id,     
       }
    )
    
#    return render_to_response('index.html')

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
   # sql = 'select id,project_title,project_content,date_format(project_startdate,"%Y-%m-%d %T") as project_startdate,date_format(project_enddate,"%Y-%m-%d %T") as project_enddate,xmjb_display,subsidized_amount,government_sector_display,xmjb_id,government_sector_id,pay_taxes_id,establishment_age_id,establishment_startdate,establishment_enddate,operation_receipt_id,zscq_count_id,zzlx_id,register_zone_id,ggsgqy_id,gyzzy_id,dzxx_id,hlw_id,znzzjqr_id,yjsdsj_id,rjqy_id,xnyyjn_id,xcl_id,whcyytyyl_id,jnhb_id,dzsw_id,ylqx_id,xnyqc_id,smjkxyy_id,jzzz_id,fs_id,zb_id,hkht_id,hycy_id,stxf_id,jj_id,hjzb_id,yj_id,my_id,wlccgyl_id,jry_id,kydw_id,ggfw_id,gjsfw_id,ctfwy_id,zjfw_id,ny_id,jgqy_id,qt_id,bx_id from projects  limit '  +  start + ','  + end
   # sql_count = 'select count(*)  from app01_project_table '
    
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

def addProject(request):
    postData = request.POST
    username = request.session.get('username','anybody') 
    dict = {
        'organizationCode' : postData.get('organizationCode'),
        'areaNumber' : postData.get('areaNumber'),
        'enterpriseName' : postData.get('enterpriseName'),
        'natureOfCorporation' : postData.get('natureOfCorporation'),
        'corporateGenderId' : postData.get('corporateGenderId'),
        'birthday' : postData.get('birthday'),
        'educationId' : postData.get('educationId'),
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
    
#    models.statistics.objects.create(**dict)   
     
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