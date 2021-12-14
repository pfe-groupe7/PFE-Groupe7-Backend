from django.db.models.fields import IntegerField
from django.db.models.query_utils import PathInfo
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse, response
from django.core import serializers
import json
from PFE.models import Ad, AdsCampusLocation, Campus, Location,Media,Category,User


# Create your views here.

# create an adscampus and media in the same method or not?
def createAd(request):
    if request.method=='POST':
        j = json.loads(request.body.decode())
        #ad = Ad(**j)
        print(j['category']+'   '+j['campus']+'   '+j['status'])
        print(j['userId'])
        print('location '+j['location'])
        #print(ad.status)
        try:
            #insert ad for user with id 1 for testing
            FKcategory = findCategoryById(j['category'])
            FKuser = getUserById(j['userId'])
            FKcampus = findCampusById(j['campus'])
            Fklocation = findLocationById(j['location'])
           

            print('Category name got :'+FKcategory.categoryName)
            print('user name got : '+FKuser.firstname)
            print('Location got: '+Fklocation.name)
            #print(FKcampus)
            # default status is pending.
            if j['price']:
                newAd = Ad(status=j['status'],title=j['title'],description=j['description'],state=Ad.State.PENDING,price=j['price'],seller=FKuser,category=FKcategory)
            else:
                newAd = Ad(status=j['status'],title=j['title'],description=j['description'],state=Ad.State.PENDING,price = 0,seller=FKuser,category=FKcategory)
            newAd.save()
            #insert adsCampus
            newAdsCampusLoc = AdsCampusLocation(ad = newAd, campus = FKcampus,location=Fklocation)
        #insert localisation (wait for frontend fix)

            newAdsCampusLoc.save()  
            response_data = 'Ad added'
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
            allAds =serializers.serialize('json', allAds)
            all="{"
            allCampus=""
            allCatgory=""
            allMedia=""
            # for a in allAds :
            #     media=getMediaByAdId(a.id)
            #     category=a.category
            #     campus=AdsCampus.objects.filter(ad=a.id).first()
            #     allMedia+=f'\"{a.id}\":'+serializers.serialize('json', media)+','#### add media foreach ad
            #     allCatgory+=f'\"{category.id}\":[{{\"name\":\"{category.categoryName}\",\"id\":\"{category.id}\",\"ad\":\"{a.id}\"}}],'#### add category
            #     allCampus+=f'\"{campus.id}\":[{{\"id\":\"{campus.id}\",\"name\":\"{campus.campus.campusName}\",\"ad\":\"{a.id}\"}}],'#### add campus

            # all+="\"campus\":{"+allCampus[:-1]+"},\"category\":{"+allCatgory[:-1]+"},\"medias\":{"+allMedia[:-1]+"},\"ads\":"+joined+"}"
            allCampus=serializers.serialize('json', Campus.objects.all())
            adsCampus=serializers.serialize('json', AdsCampusLocation.objects.all())
            allCatgory=serializers.serialize('json', Category.objects.all())
            allMedia=serializers.serialize('json', Media.objects.all())
            all+="\"adsCampus\":"+adsCampus+",\"campus\":"+allCampus+",\"categories\":"+allCatgory+",\"medias\":"+allMedia+",\"ads\":"+allAds+"}"
            print(allAds)

            return HttpResponse(all,content_type='applicatoin/json',status=200)
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
                AdsCampusLocation.objects.filter(ad=id).delete()
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

def findCategoryById(id):
    try:
        category = Category.objects.get(pk=id)
        return category
    except:
        return NameError

def findCampusById(id):
    try:
        campus = Campus.objects.get(pk = id)
        return  campus

    except:
        return NameError

def getUserById(id):
        try:
            j = User.objects.get(pk=id)
           
            return j
        except:
          return HttpResponse(status=500)
def findLocationById(id):
    try:
        j = Location.objects.get(pk=id)
        return j
    except:
        return HttpResponse(status=404)

