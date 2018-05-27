from django.shortcuts import render
from BeautyWorld.models import *
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers
import json
# Create your views here.
#body_unicode = request.body.decode('utf-8')
#body = json.loads(body_unicode)
#content = body['t1']


def category(request):
    try:
        categories =Category.objects.all().values()
        data = list(categories)
        return JsonResponse({"code": 0, "data": data})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1})

