from django.db.models.fields import IntegerField
from django.db.models.query_utils import PathInfo
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, response
from django.core import serializers
import json
from PFE.models import Ad, AdsCampus,Media,Category

# Create your views here.

# create an adscampus and media in the same method or not?
def createAd(request):
    if request.method=='POST':
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
    else:
        return HttpResponse(HttpResponse=400)

#Assume that every updatable fields must be filled in frontend. Must be able to edit campus (in adscampus)
def editAd(request,id):
    if request.method=='PUT':
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
    else:
        return HttpResponse(status=400)
     


def getAllAds(request):
    if request.method=='GET':
        try:
            allAds=Ad.objects.all()
            joined =serializers.serialize('json', allAds)
            medias="{"
            for a in allAds :
                media=getMediaByAdId(a.id)
                category=a.category
                campus=AdsCampus.objects.filter(ad=a.id).first()
                medias +=f'\"{a.id}\":'+serializers.serialize('json', media)+','#### add media foreach ad
                medias+=f'\"category\":[{{\"name\":\"{category.categoryName}\",\"id\":\"{category.id}\"}}],'#### add category
                medias+=f'\"campus\":[{{\"id\":\"{campus.id}\",\"name\":\"{campus.campus.campusName}\",\"ad\":\"{a.id}\"}}],'#### add campus

            medias+="\"ads\":"+joined+"}"+""
        
            return HttpResponse(medias,content_type='applicatoin/json',status=200)
        except:
            return HttpResponse(status=500)
    else:
            return HttpResponse(status=400)    

# return also adscampus or campus
def getAdById(request,id):
    if request.method == 'GET':
        try:
            print(id)
            j = Ad.objects.get(pk=id)
            ad  = serializers.serialize('json',[j],ensure_ascii=False)
            print(ad)
            return HttpResponse(ad,content_type='application/json',status=200)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)
    
def deleteAd(request,id):
    if request.method=="DELETE":
        try:
            print('delete ad id:')
            print(id)
            
            #first delete the media and adcampus associated to this ad
            if Ad.objects.filter(pk=id):
                Media.objects.filter(ad=id).delete()
                print('media deleted')
                AdsCampus.objects.filter(ad=id).delete()
                print('adscampus deleted')
                Ad.objects.filter(pk=id).delete()
                response_data = 'ad deleted'
                return HttpResponse(json.dumps(response_data),content_type='applicatoin/json',status=200)
            else:
                print('Ad not found')
                return HttpResponse(status=404) 
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)

######
# 
def getMediaByAdId(id):
   
      try:
          j = Media.objects.filter(ad_id=id)

          return j
      except:
          return -1  

