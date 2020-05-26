from django.shortcuts import render
from anaconda_navigator.utils.py3compat import request
from django.http import  HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
def Index(request):
    return render_to_response('index.html')
    