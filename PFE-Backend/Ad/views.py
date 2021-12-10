from django.db.models.fields import IntegerField
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, response
from django.core import serializers
import json
from Ad.models import Ad

# Create your views here.


def createAd(request):
    j = json.loads(request.body.decode())
    ad = Ad(**j)
    # default status is pending.
    print(ad.status)
    try:
        ad.save()
        response_data = 'Ad added '+ad.title
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
    except:
        return HttpResponse(status=500)

#Assume that every updatable fields must be filled in frontend
def editAd(request,id):
    try:
      print(id)
      newData = json.loads(request.body.decode())
      if newData['title']!='':
         Ad.objects.filter(pk=id).update(title=newData['title'])
      if newData['status']!='':  
         Ad.objects.filter(pk=id).update(status=newData['status'])
      if newData['state']!='':  
         Ad.objects.filter(pk=id).update(state=newData['state'])  
      if newData['description']!='':
          Ad.objects.filter(pk=id).update(description=newData['description'])
      if newData['price']!='':
          Ad.objects.filter(pk=id).update(price=newData['price'])  
          
      print('updated')
      response_data = 'data updated'
      return HttpResponse(json.dumps(response_data),content_type='application/json',status=200)
    except:
        return HttpResponse(status=500)    


def getAllAds(request):
    try:
        allAds =serializers.serialize('json', Ad.objects.all())
        print(allAds)
        return HttpResponse(allAds,content_type='applicatoin/json',status=200)
    except:
        return HttpResponse(status=500)

def getAdById(request,id):
    try:
        print(id)
        j = Ad.objects.get(pk=id)
        ad  = serializers.serialize('json',[j],ensure_ascii=False)
        print(ad)
        return HttpResponse(ad,content_type='application/json',status=200)
    except:
        return HttpResponse(status=500)
    
