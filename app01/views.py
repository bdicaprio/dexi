from django.shortcuts import render
from anaconda_navigator.utils.py3compat import request
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from app01 import models
from _cffi_backend import string
from django.db import connection
import json

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
    
    print('id',username_id)
    return render(
        request,
        "index.html", 
        {
        "result":result,  
        "username_id":username_id,     
       }
    )
    
#    return render_to_response('index.html')

def getprojectlist(request):
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
    print(col_names)
    result = []
    
    for row in rawData:
        print(row)
        objDict = {}
        
        for index, value in enumerate(row):           
            objDict[col_names[index]] = value       
    
        result.append(objDict)
    cursor.execute(sql_count)
    count = cursor.fetchall()
    count = count[0][0]      
    dict = {"code":0,"msg":"","count":count,"data":result}
    return HttpResponse(json.dumps(dict), content_type="application/json")