# Create your models here.
from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser
import datetime
import django.utils as ut


#class UserManager(BaseUserManager):
#    def create_user(self, email, password, firstname, lastname, phone):
#        if email and password and firstname and lastname and phone:
#            user = self.model(email=self.normalize_email(email), firstname=firstname, lastname=lastname, phone=phone)
#            user.set_password(password)
#            user.save(using=self._db)
#            return user
#
#    def create_superuser(self, email, password):
#        """
#        Creates and saves a superuser with the given email, date of
#        birth and password.
#        """
#        user = self.create_user(email,
#                                password=password,
#                                firstname="admin",
#                                lastname="adminovich",
#                                phone="88005553535"
#                                )
#        user.save(using=self._db)
#        return user
#
#    def update_user(self, user_id, email, password, firstname, lastname, phone):
#        user = User.objects.get(pk=user_id)
#        user.email = self.normalize_email(email)
#        user.set_password(password)
#        user.firstname = firstname
#        user.lastname = lastname
#        user.phone = phone
#        user.save(using=self._db)
#
#
#class User(AbstractBaseUser):
#    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
#    phone = models.CharField(verbose_name='phone', max_length=11, default="")
#    firstname = models.CharField(verbose_name='firstname', max_length=255, default="")
#    lastname = models.CharField(verbose_name='lastname', max_length=255, default="")
#    is_staff = models.BooleanField(verbose_name='is_staff', default=False)
#    is_superuser = models.BooleanField(verbose_name='is_staff', default=False)
#    objects = UserManager()
#
#    USERNAME_FIELD = 'email'
#    REQUIRED_FIELDS = []
#
#    def get_full_name(self):
#        return self.firstname + self.lastname
#
#    def get_short_name(self):
#        return self.firstname
#
#    def has_perm(self, perm, obj=None):
#        return self.is_superuser
#
#    def has_module_perms(self, app_label):
#        return self.is_superuser
#
#


class Credentials(models.Model):
    email = models.CharField(verbose_name='email', max_length=255, default="", null=True)
    password = models.CharField(verbose_name='password', max_length=255, default="")
    phone = models.CharField(verbose_name='phone', max_length=255, default="")
    vk_id = models.CharField(verbose_name='image_url', max_length=1000, default="", null=True)


class PersonalDetails(models.Model):
    name = models.CharField(verbose_name='name', max_length=255, default="")
    surname = models.CharField(verbose_name='surname', max_length=255, default="")
    birth_date = models.DateTimeField(verbose_name='birth_date', default=ut.timezone.now)
    phone = models.CharField(verbose_name='phone', max_length=255, default="")
    vk_id = models.CharField(verbose_name='image_url', max_length=1000, default="", null=True)


class Master(models.Model):
    details = models.ForeignKey(PersonalDetails, null=False)
    description = models.CharField(verbose_name='description', max_length=1000, default="")
    image_url = models.CharField(verbose_name='description', max_length=1000, default="")


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


