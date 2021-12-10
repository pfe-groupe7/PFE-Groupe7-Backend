from django.http.response import HttpResponsePermanentRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core import serializers
import json
from PFE.models import User


def login(request):
    j = json.loads(request.body.decode())
    user = User(**j)
    res = User.objects.filter(email=user.email)
    token = Token.generate_key()  # Token.objects.create(user=res.first().firstname)
    if(res.count() != 0):
        return HttpResponse(content=json.dumps({"token": token, "user": {"firstname": res.first().firstname, "lastname": res.first().lastname}}), content_type="application/json")

    else:
        return HttpResponse(status=404)


def register(request):
    j = json.loads(request.body.decode())
    user = User(**j)
    print(user)
    try:
        print(j)
        user.save()
        response_data = "test-register"
        return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
    except:
        return HttpResponse(status=409)


def getUserById(request, id):
    try:
        print(id)
        j = User.objects.get(pk=id)
        user = serializers.serialize('json', [j], ensure_ascii=False)
        print(user)
        return HttpResponse(user, content_type='application.json', status=200)
    except:
        return HttpResponse(status=500)


def getAllUsers(request):
    try:
        users = User.objects.all()
        users = serializers.serialize('json', users, ensure_ascii=False)
        print(users)
        return HttpResponse(users, content_type='application.json', status=200) 
    except:
        return HttpResponse(status=500)
        

def editUser(request, id):
    try:
        print(id)
        newData = json.loads(request.body.decode())
        if newData['campus'] != '':
            User.objects.filter(pk=id).update(campus=newData['campus'])
        if newData['password'] != '':
            User.objects.filter(pk=id).update(password=newData['password'])
        print('Updated')
        response_data = 'User updated'
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
    except:
        return HttpResponse(status=500)

# Test function
def Hello(request):
    return HttpResponse("Welcome Backend")
