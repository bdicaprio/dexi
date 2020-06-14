"""dexi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),    
    url(r'^authlogin/', views.authlogin),       
    url(r'^index/', views.index),
    url(r'^getprojectlist/', views.getPojectList),
    url(r'^addProject/', views.addProject),
    url(r'^saveProject/', views.saveProject),     
    url(r'^addCompany/', views.addCompany),    
    url(r'^addEconomic/', views.addEconomic), 
    url(r'^addPersonnel/', views.addPersonnel), 
    url(r'^addActivities/', views.addActivities),
    url(r'^addStatistics/', views.addStatistics),
    url(r'^delProject/', views.delProject),    
    url(r'^member/', views.member),   
    url(r'^saveUserinfo/', views.saveUserinfo),   
    url(r'^changepasswd/', views.changepasswd),   
    url(r'^changePassword/', views.changePassword),
    url(r'^membermanager/', views.membermanager), 
    url(r'^getuserinfo/', views.getuserinfo),
    url(r'^torchgather/', views.torchgather),
    url(r'^getStatistics/', views.getStatistics),  
    url(r'^getCompany/', views.getCompany),
    url(r'^getEconomic/', views.getEconomic),
    url(r'^getPersonnel/', views.getPersonnel),  
    url(r'^getProjects/', views.getProjects),
    url(r'^getActivities/', views.getActivities),
    url(r'^addUser/', views.addUser),   
    url(r'^saveUser/', views.saveUser), 
    url(r'^editUser/', views.editUser),
    url(r'^delUser/', views.delUser),
    url(r'^getcompanyinfo/', views.getcompanyinfo),   
    url(r'^delCompany/', views.delCompany),        
    url(r'^createExcel/', views.createExcel),     
        
     
    
                                                              
]
