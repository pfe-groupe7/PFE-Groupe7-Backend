# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from django.http import HttpResponse
from django.core import serializers
import json
from testo.models import User


def login(request) :
   print(request)
   response_data="test-login"   
   res=json.dumps(serializers.serialize("json",User.objects.filter(email="test1@vinci.be")))
   return HttpResponse(res, content_type="application/json")


def register(request):
    print(request.body.decode())
    
    u= User(firstname="test-firstname",lastname="lastname",email="test1@vinci.be",moderator=True,password="123")
    u.save()
    response_data="test-register" 
    return HttpResponse(json.dumps(response_data), content_type="application/json")    
















  