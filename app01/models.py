from django.db import models

# Create your models here.
class user(models.Model):
    id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=16,blank=True,null=True)
    password = models.CharField(max_length=16,blank=True,null=True)
    name = models.CharField(max_length=16,blank=True,null=True)
    nickname = models.CharField(max_length=16,blank=True,null=True)
    sex = models.BooleanField()
    telephone = models.IntegerField(blank=True,null=True)
    email = models.EmailField()
    company = models.CharField(max_length=16,blank=True,null=True) 
    remarks = models.TextField(blank=True,null=True)

class enterpriseStatistics(models.Model):
    organizationCode = models.CharField(max_length=16,blank=True,null=True)
    areaNumber = models.CharField(max_length=16,blank=True,null=True)
    enterpriseName = models.CharField(max_length=16,blank=True,null=True)
    natureOfCorporation = models.CharField(max_length=16,blank=True,null=True)
    corporateGender = models.BooleanField()
    birthday = models.DateTimeField(blank=True,null=True)
    education = models.BooleanField()
    address = models.CharField(max_length=64,blank=True,null=True)
    postalCode = models.IntegerField(blank=True,null=True)
    registeredAddress = models.CharField(max_length=64,blank=True,null=True)
    manager = models.CharField(max_length=16,blank=True,null=True)
    telephone = models.IntegerField(blank=True,null=True)
    fax = models.IntegerField(blank=True,null=True)
    statisticalControlOfficer = models.CharField(max_length=16,blank=True,null=True)
    preparedBy = models.CharField(max_length=16,blank=True,null=True)
    preparedByTelephone = models.CharField(max_length=16,blank=True,null=True)
    fillingTime = models.DateTimeField(blank=True,null=True)
    email = models.EmailField()
    url = models.CharField(max_length=16,blank=True,null=True)
    preparedByMobilephone = models.CharField(max_length=16,blank=True,null=True)
    

class companyProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,blank=True,null=True)
    code = models.CharField(max_length=16,blank=True,null=True)
    content = models.TextField(blank=True,null=True) 

class economicOverview(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,blank=True,null=True)
    unit = models.CharField(max_length=8,blank=True,null=True)
    code = models.CharField(max_length=16,blank=True,null=True)
    number = models.IntegerField(blank=True,null=True)
    
class personnelProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,blank=True,null=True)
    unit = models.CharField(max_length=8,blank=True,null=True)
    code = models.CharField(max_length=16,blank=True,null=True)
    number = models.IntegerField(blank=True,null=True)
    
class technologyProjects(models.Model):
    id = models.AutoField(primary_key=True)  
    projectName = models.CharField(max_length=64,blank=True,null=True)   
    projectFrom = models.CharField(max_length=64,blank=True,null=True)   
    DevelopmentForm = models.CharField(max_length=64,blank=True,null=True)
    AchievementDisplay = models.CharField(max_length=64,blank=True,null=True)
    EconomicGoals = models.CharField(max_length=64,blank=True,null=True)
    activityType = models.CharField(max_length=64,blank=True,null=True)
    startTime = models.DateTimeField(blank=True,null=True)
    endTime = models.DateTimeField(blank=True,null=True)
    personnel =  models.CharField(max_length=64,blank=True,null=True)
    time = models.CharField(max_length=64,blank=True,null=True)
    stage = models.CharField(max_length=64,blank=True,null=True)
    funds = models.IntegerField(blank=True,null=True)
    capital = models.IntegerField(blank=True,null=True)
    
class technologicalActivities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64,blank=True,null=True)
    unit = models.CharField(max_length=8,blank=True,null=True)
    code = models.CharField(max_length=16,blank=True,null=True)
    number = models.IntegerField(blank=True,null=True)