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

def sign_up(request):
    try:
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)

        res = create_user(body["phone"],body["password"],body["repeat_password"])
        if res[0] is None:
            return 
        data = list(categories)
        return JsonResponse({"code": 0, "data": data})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "message":str(e)})


def create_user(phone, password, rep_password):
    if(password != rep_password):
        return (None,"Пароли не совпадают")
    if Credentials.objects.get(phone=phone,password=password) is None:
        cred = Credentials()
        cred.phone = phone
        cred.password = password
        cred.save()

        client = Client(credentials=cred)
        client.save()
        return (client,"")
    else:
        return (None, "Такой пользователь уже существует")






def get_user(phone, password):
    if (Credentials.objects.get(phone=phone,password=password) is None):
        pass
