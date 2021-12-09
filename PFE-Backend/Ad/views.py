from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core import serializers
import json
from PFE.models import Ad

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
