from django.shortcuts import render
from BeautyWorld.models import *
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.core import serializers
import json


def api_category(request):
    try:
        categories = Category.objects.all().values()
        data = list(categories)
        return JsonResponse({"code": 0, "data": data})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})


def api_salon(request):
    try:
        salons = get_salons()
        data = list(salons)
        return JsonResponse({"code": 0, "data": data})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})


def sign_up(request):
    try:
        phone = request.POST["phone"]
        password = request.POST["password"]
        res = create_user(phone, password)
        if res[0] is None:
            return JsonResponse({"code": 1, "data": {"code": 1, "message": res[1]}})
        else:
            return JsonResponse({"code": 0, "data": res[0]})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})


def sign_in(request):
    try:
        phone = request.POST["phone"]
        password = request.POST["password"]
        if not Credentials.objects.filter(phone=phone, password=password).exists():
            return JsonResponse({"code": 1, "data": {"code": 1, "message": "Такого пользователя нет"}})
        else:
            cred = Credentials.objects.filter(phone=phone, password=password).first()

            return JsonResponse({"code": 0, "data": get_client(cred)})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})

def set_favorite(request):
    try:
        return JsonResponse({"code": 0})

    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})


def api_cart(request):
    try:
        ids = eval(request.POST["categories"])
        client = Client.objects.get(id=request.POST["id"])
        new_cart = Cart(client=client)
        new_cart.closed = True
        new_cart.save()
        for id in ids:
            service = Category.objects.get(pk=id)
            new_cart.categories.add(service)
        new_cart.save()
        return JsonResponse({"code": 0, "data": new_cart.id})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})


def api_orders(request):
    try:
        id = request.GET['id']
        client = Client.objects.get(pk=id)

        return JsonResponse({"code": 0, "data": get_closed_carts(client.id)})
    except Exception as e:
        print(e)
        return JsonResponse({"code": 1, "data": {"code": 1, "message": str(e)}})

def create_user(phone, password):
    if Credentials.objects.filter(phone=phone, password=password).count() == 0:
        cred = Credentials()
        cred.phone = phone
        cred.password = password
        cred.save()

        client = Client(credentials=cred)
        client.save()
        client_id = client.id
        cart = Cart(client=Client.objects.get(id=client_id))
        cart.save()
        return get_client(cred), ""
    else:
        return None, "Такой пользователь уже существует"


def get_salons():
    #if cred is None:
    salons = Salon.objects.all().values()
    #else:
    #    salons = Client.objects.filter(credentials=cred).first().favorite_salons.all().values()
    for sal in salons:
        sal = get_salon_info(sal)
    return salons

def get_salon_info(sal):
    urls = list(Photo.objects.filter(salon=sal["id"]).values())
    sal["urls"] = urls
    urls_array = []
    for url in urls:
        urls_array.append(url["url"])
    sal["urls_array"] = urls_array
    sal["masters"] = get_masters(sal["id"])

    services = list(Service.objects.filter(salon=Salon.objects.get(pk=sal["id"])).values())
    for serv in services:
        serv["category"] = Category.objects.filter(pk=serv["category_id"]).values().first()
    sal["services"] = services
    return sal


def get_masters(salon_id):
    if salon_id is None:
        masters = Master.objects.all().values()
    else:
        masters = Master.objects.filter(salon=salon_id).values()
    for mast in masters:
        mast["details"] = get_details(mast["id"])
    return list(masters)


def get_details(pers_id):
    details = PersonalDetails.objects.filter(pk=pers_id).values().first()
    return details



#def get_closed_carts(cred):
#    client = Client.objects.get(credentials=cred)
#    cart = Cart.objects.filter(client=client,order__isnull=True).values().first()
#    services = list(Cart.objects.get(client=client,order=None).services.all().values())
#    cart["services"] = services
#    services_ids = []
#    for serv in services:
#        services_ids.append(serv["id"])
#    cart["services_ids"] = services_ids
#    return cart

def get_closed_carts(client_id):
    carts = list(Cart.objects.filter(client=client_id,closed=True).values())
    for cart in carts:
        orders_array = Order.objects.filter(cart=cart["id"]).values()
        for order in orders_array:
            salon_id = order["salon_id"]
            order["salon"]=Salon.objects.filter(pk=salon_id).values().first()
            master_id = order["master_id"]
            master = Master.objects.filter(pk=master_id).values().first()
            master["details"] = get_details(master["id"])
            order["master"]=master
            order_obj = Order.objects.get(pk=order["id"])
            servs = order_obj.services.all().values()
            order["services"] = list(servs)
        cart["orders"] = list(orders_array)
        cart_obj = Cart.objects.get(pk=cart["id"])
        categories = list(cart_obj.categories.all().values())
        categories_ids = []
        for cat in categories:
            categories_ids.append(cat["id"])
        #cart["categories"]=categories
        cart["categories_ids"] = categories_ids
    return list(carts)



def get_cart(cred):
    client = Client.objects.get(credentials=cred)
    cart = Cart.objects.filter(client=client,order__isnull=True).values().first()
    services = list(Cart.objects.get(client=client,order=None).services.all().values())
    cart["services"] = services
    services_ids = []
    for serv in services:
        services_ids.append(serv["id"])
    cart["services_ids"] = services_ids
    return cart

def get_orders(cred):
    client = Client.objects.get(credentials=cred)
    carts = list(Cart.objects.exclude(order__isnull = True).filter(client=client).values())
    for cart in carts:
        order_obj = Order.objects.filter(pk=cart["order_id"]).values().first()
        order_obj["status"] = OrderStatus.objects.filter(pk=order_obj["status_id"]).values().first()
        services = list(Cart.objects.get(pk=cart["id"]).services.all().values())
        services_ids = []
        for serv in services:
            serv["salon"] = get_salon_info(Salon.objects.filter(pk=order_obj["salon_id"]).values().first())
            services_ids.append(serv["id"])
        cart["services_ids"] = services_ids
        cart["services"] = services
        cart["order"] = order_obj

    return carts

def get_client(cred):
    client = Client.objects.filter(credentials=cred).values().first()


    #carts = get_closed_carts(client["id"])

    client_obj = Client.objects.get(credentials=cred)
    client["credentials"] = Credentials.objects.filter(pk = cred.id).values().first()
    #salons = list(get_salons(cred))
    salons_ids = []
    for sl in Client.objects.filter(credentials=cred).first().favorite_salons.all():
        salons_ids.append(sl.id)
    client["favorite"] = salons_ids
    client["filters"] = Client.objects.filter(credentials=cred).values("high_price","place_flag","company_flag","max_distance").first()

    #client["favorite"] = salons
    #carts_closed_ids = []
    #for crt in Cart.objects.filter(client=client_obj,order=None,closed=True):
    #    carts_closed_ids.append(crt.id)
    #client["current_cart"] = Cart.objects.filter(client=client_obj,closed=False).first().id
    #client["closed_carts"] = get_closed_carts(client_obj.id)
    #orders_ids=[]
    #for ord in Cart.objects.filter(client=client_obj).exclude(order=None,closed=False):
    #    orders_ids.append(ord.id)
    #client["carts_with_orders"] = orders_ids
    return client

#def orders