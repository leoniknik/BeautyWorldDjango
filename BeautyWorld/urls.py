from django.conf.urls import url, include
from BeautyWorld.views import category, sign_up, sign_in, salon, cart
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

    url(r'^category$', category),  # GET
    url(r'^salon$', salon),  # GET
    url(r'^signup$', sign_up),  # POST
    url(r'^signin$', sign_in),  # POST
    url(r'^cart$', cart),  # POST
    #url(r'^orders$', orders),  # GET
]