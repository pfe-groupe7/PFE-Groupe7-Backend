from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core import serializers
import json
from PFE.models import User


def login(request) :
    j=json.loads(request.body.decode())
    u=User(**j)
    res=User.objects.filter(email=u.email)
    token =Token.generate_key()# Token.objects.create(user=res.first().firstname)
    if(res.count()!=0):
         return HttpResponse(content=json.dumps({"token":token,"user":{"firstname":res.first().firstname,"lastname":res.first().lastname}}), content_type="application/json")
 
    else:
         return HttpResponse(status=404) 


def register(request):
    j=json.loads(request.body.decode())
    u=User(**j)
    res=User.objects.filter(email=u.email).update()
    print(u)
    try:
        u.save()
        response_data="Utilisateur bien ajouté" 
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)   
    except:
        return HttpResponse(status=409) 
        
def update(request):
    # j=json.loads(request.body.decode())
    u=User()
    print(type(u))
    try:
        u.save()
        response_data="Votre profil a été bien modifié" 
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=200)   
    except:
        return HttpResponse(status=409) 

def Hello(request):
    return HttpResponse("Welcome Backend")    
     
















  