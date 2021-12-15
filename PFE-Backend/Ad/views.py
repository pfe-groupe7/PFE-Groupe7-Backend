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

def addMedia(request):
    if request.method=='POST':
        try:
            newData = json.loads(request.body.decode())
            print('url got: '+newData['url'])
            newAd = Ad.objects.last()
            print('id of new ad: ')
            print(newAd.id)
            newMedia = Media(url=newData['url'],ad=newAd)
            newMedia.save()
            response_data = 'media added'
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
        except:
             return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)
    

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
            adId=id
            newData = json.loads(request.body.decode())
            print("before")
             
   
           
            # print("after")
            # if newData['title']!='':
            #     print("title")
            #     Ad.objects.filter(id=adId).update(title=newData['title'])
            # if newData['status']!='':  
            #     print("statu")
            #     Ad.objects.filter(id=adId).update(status=newData['status'])
            if newData['state']!='':  
                print(newData)
                Ad.objects.filter(id=adId).update(state=newData['state'])  
            # if newData['description']!='':
            #     Ad.objects.filter(id=adId).update(description=newData['description'])
            # if newData['price']!='':
            #     Ad.objects.filter(id=adId).update(price=newData['price'])  
                
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
            allUser=serializers.serialize('json', User.objects.all())
            allLocations=serializers.serialize('json', Location.objects.all())
            all+="\"adsCampus\":"+adsCampus+",\"campus\":"+allCampus+",\"locations\":"+allLocations+",\"users\":"+allUser+",\"categories\":"+allCatgory+",\"medias\":"+allMedia+",\"ads\":"+allAds+"}"
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
            all="{"
            category=serializers.serialize('json',Category.objects.filter(pk=j.category.id))
            user=serializers.serialize('json',User.objects.filter(pk=j.seller.id))
            adsCampusLoc=AdsCampusLocation.objects.filter(ad=id)
            location=adsCampusLoc[0].location.name
            print(location)
            adsCampus=serializers.serialize('json',adsCampusLoc)
            campus=serializers.serialize('json',Campus.objects.all())
            medias=serializers.serialize('json',getMediaByAdId(id))
            ad  = serializers.serialize('json',[j],ensure_ascii=False)
            print(location)
            all+="\"campus\":"+campus+",\"category\":"+category+",\"location\": \""+location+"\",\"adsCampus\":"+adsCampus+",\"medias\":"+medias+",\"ads\":"+ad+",\"seller\":"+user+"}"
           
            return HttpResponse(all,content_type='application/json',status=200)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)
    
def deleteAd(request,id):
   
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
def getallCategory(request):
    if request.method=="GET":
        try:
        
            return HttpResponse(serializers.serialize('json',Category.objects.all()),content_type='applicatoin/json',status=200)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)

