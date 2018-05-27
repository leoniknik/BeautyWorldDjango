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
        return JsonResponse({"code": 1, "data":{ "code":1,"message":str(e)}})

def salon(request):
    try:
        salons = Salon.objects.all().values()
        for sal in salons:
            urls = list(Photo.objects.filter(salon=sal["id"]).values())
            sal["urls"] = urls
            urls_array = []
            for url in urls:
                urls_array.append(url["url"])
            sal["urls_array"] = urls_array
        data = list(salons)
        return JsonResponse({"code": 0, "data": data})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data":{ "code":1,"message":str(e)}})

def sign_up(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        res = create_user(body["phone"],body["password"])
        if res[0] is None:
            return JsonResponse({"code": 1, "data":{ "code":1,"message":res[1]}})
        else:
            return JsonResponse({"code": 0, "data": res[0]})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data":{ "code":1,"message":str(e)}})


def sign_in(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if not Credentials.objects.filter(phone=body["phone"], password=body["password"]).exists():
            return JsonResponse({"code": 1, "data":{ "code":1,"message":"Такого пользователя нет"}})
        else:
            cred = Credentials.objects.filter(phone=body["phone"], password=body["password"]).first()
            client = Client.objects.filter(credentials=cred).values().first()
            client["credentials"] = Credentials.objects.filter(phone=body["phone"], password=body["password"]).values().first()
            return JsonResponse({"code": 0, "data": client})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data":{ "code":1,"message":str(e)}})


def create_user(phone, password):
    if not Credentials.objects.filter(phone=phone,password=password).exists():
        cred = Credentials()
        cred.phone = phone
        cred.password = password
        cred.save()

        client = Client(credentials=cred)
        client.save()
        client_id = client.id
        return (Client.objects.get(id=client_id),"")
    else:
        return (None, "Такой пользователь уже существует")

