from django.conf.urls import url, include
from BeautyWorld.views import api_category, sign_up, sign_in, api_salon, api_cart, api_orders
urlpatterns = [
    #url(r'^signin$', signin),  # POST
    #url(r'^signup$', signup),  # POST
    #url(r'^edit_user$', edit_user),  # POST
    #url(r'^add_vehicle$', add_vehicle),  # POST
    #url(r'^edit_vehicle$', edit_vehicle),  # POST
    #url(r'^get_list_of_actual_crashes$', get_list_of_actual_crashes),  # GET
    #url(r'^get_list_of_history_crashes$', get_list_of_history_crashes),  # GET
    #url(r'^get_list_of_offers$', get_list_of_offers),  # GET
    #url(r'^get_list_of_vehicles$', get_list_of_vehicles),  # GET

    url(r'^category$', api_category),  # GET
    url(r'^salon$', api_salon),  # GET
    url(r'^signup$', sign_up),  # POST
    url(r'^signin$', sign_in),  # POST
    url(r'^cart$', api_cart),  # POST
    url(r'^orders$', api_orders),  # GET
]