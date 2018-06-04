# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
import datetime
import django.utils as ut

class Credentials(models.Model):
    email = models.CharField(verbose_name='email', max_length=255, default="", null=True)
    password = models.CharField(verbose_name='password', max_length=255, default="")
    phone = models.CharField(verbose_name='phone', max_length=255, default="")
    vk_id = models.CharField(verbose_name='vk_id', max_length=1000, default="", null=True)


class PersonalDetails(models.Model):
    name = models.CharField(verbose_name='name', max_length=255, default="")
    surname = models.CharField(verbose_name='surname', max_length=255, default="")
    birth_date = models.DateTimeField(verbose_name='birth_date', default=ut.timezone.now)
    phone = models.CharField(verbose_name='phone', max_length=255, default="")
#    vk_id = models.CharField(verbose_name='image_url', max_length=1000, default="", null=True)


class Master(models.Model):
    details = models.ForeignKey(PersonalDetails, null=False)
    description = models.CharField(verbose_name='description', max_length=1000, default="")
    image_url = models.CharField(verbose_name='image_url', max_length=1000, default="")


class Salon(models.Model):
    name = models.CharField(verbose_name='name', max_length=255, default="")
    credentials = models.ForeignKey(Credentials, null=False)
    address = models.CharField(verbose_name='address', max_length=255, default="")
    telephone = models.CharField(verbose_name='telephone', max_length=255, default="")
    url = models.CharField(verbose_name='url', max_length=255, default="")
    vk_url = models.CharField(verbose_name='vk_url', max_length=255, default="")
    description = models.CharField(verbose_name='description', max_length=1000, default="")
    schedule = models.CharField(verbose_name='schedule', max_length=1000, default="")
    longitude = models.FloatField(verbose_name='longitude', default=0)
    latitude = models.FloatField(verbose_name='latitude', default=0)
    place_flag = models.IntegerField(verbose_name='place_flag', default=0)
    company_flag = models.IntegerField(verbose_name='company_flag', default=0)
    masters = models.ManyToManyField(Master)


class Client(models.Model):
    credentials = models.ForeignKey(Credentials, null=False)
    details = models.ForeignKey(PersonalDetails, null=True)
    high_price = models.IntegerField(verbose_name='high_price', default=-1)
    place_flag = models.IntegerField(verbose_name='place_flag', default=0)
    company_flag = models.IntegerField(verbose_name='company_flag', default=0)
    max_distance = models.FloatField(verbose_name='max_distance', default=-1)
    favorite_salons = models.ManyToManyField(Salon)


class Photo(models.Model):
    salon = models.ForeignKey(Salon, null=False)
    url = models.CharField(verbose_name='url', max_length=255, default="")


class Category(models.Model):
    name = models.CharField(verbose_name='name', max_length=255, default="")
    description = models.CharField(verbose_name='description', max_length=1000, default="")
    image_url = models.CharField(verbose_name='image_url', max_length=1000, default="def url")


class Service(models.Model):
    name = models.CharField(verbose_name='name', max_length=255, default="")
    description = models.CharField(verbose_name='description', max_length=1000, default="")
    image_url = models.CharField(verbose_name='image_url', max_length=1000, default="def url")
    category = models.ForeignKey(Category, null=False)
    salon = models.ForeignKey(Salon, null=False)
    price = models.IntegerField(verbose_name='price',  default=0)


class OrderStatus(models.Model):
    status = models.CharField(verbose_name = 'status', max_length = 255, default = "")

class Cart(models.Model):
    categories = models.ManyToManyField(Category)
    client = models.ForeignKey(Client,null=False)
    closed = models.BooleanField(verbose_name = 'closed', default = False)

class Order(models.Model):
    master = models.ForeignKey(Master, null = True)
    services = models.ManyToManyField(Service)
    date = models.DateTimeField(verbose_name = 'date', default = ut.timezone.now)
    status = models.ForeignKey(OrderStatus, null = False)
    salon = models.ForeignKey(Salon, null = False)
    info = models.CharField(verbose_name = 'info', max_length = 2000, default = "")
    cart = models.ForeignKey(Cart,null=False)


class Feedback(models.Model):
    points = models.IntegerField(verbose_name="points", default=0)
    comment = models.CharField(verbose_name="comment", max_length=1000, default="")
    client = models.ForeignKey(Client, null=False)
    order = models.ForeignKey(Order, null=False)

