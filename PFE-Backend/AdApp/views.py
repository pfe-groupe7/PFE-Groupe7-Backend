from django.shortcuts import render
from django.http import HttpResponse
import json
from PFE.models import User
from AdApp.models import Ad

# Create your views here.

def createAd(request):
    j = json.loads(request.body.decode())
    ad = Ad(**j)
    ad.state = ad.State.PENDING
    print(ad)
    try:
        ad.save()
        response_data = 'test-createAd'
        return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
    except:
        return HttpResponse(status=500)

#def updateAd(request, id):
    ad = Ad.objects.get(id=id)




#def deleteAd(request): 





