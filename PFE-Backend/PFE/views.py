from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core import serializers
import json
from PFE.models import User,Ad,Campus,Location


def login(request):
    j = json.loads(request.body.decode())
    u = User(**j)
    res = User.objects.filter(email=u.email)
    token = Token.generate_key()  # Token.objects.create(user=res.first().firstname)
    if(res.count() != 0):
        return HttpResponse(content=json.dumps({"token": token, "user": {"firstname": res.first().firstname, "lastname": res.first().lastname}}), content_type="application/json")

    else:
        return HttpResponse(status=404)


def register(request):
    j = json.loads(request.body.decode())
    u = User(**j)
    print(u)
    try:
        u.save()
        response_data = "test-register"
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
    except:
        return HttpResponse(status=409)


# Test function
def Hello(request):
    return HttpResponse("Welcome Backend")

def insertTestData(request):
    woluwe = Campus(campusName='Nivelles')
    woluwe.save()
    loc1 = Location(name='UCL main campus', address='how am I supposed to know?', campus = woluwe )
    loc2 = Location(name='Institut Paul Lambin',address='Ok I should probably know but well...',campus = woluwe)
    loc1.save()
    loc2.save()
    u1 = User(email='nohorny@gmail.com',lastname = 'horny',firstname ='no',campus = woluwe, password='hoooorrny', moderator=True)
    u2 = User(email='hornyjail@gmail.com',lastname = 'horny',firstname ='jail',campus = woluwe, password='hoooorrny', moderator=False)
    u1.save()
    u2.save()
    ad1 = Ad(status = Ad.Status.TOSELL, title ='ad1', description= 'this is ad1',price = 69, seller = u1)
    ad2 = Ad(status = Ad.Status.TOSELL, title ='ad2', description= 'this is ad2',price = 69, seller = u1)
    ad3 = Ad(status = Ad.Status.TOSELL, title ='ad3', description= 'this is ad3',price = 69, seller = u2)
    ad4 = Ad(status = Ad.Status.TOSELL, title ='ad4', description= 'this is ad4',price = 69, seller = u2)
    ad1.save() 
    ad2.save()
    ad3.save()
    ad4.save()
    return HttpResponse("Oh you just added some stuff in the db")