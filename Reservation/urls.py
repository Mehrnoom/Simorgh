from django.views.generic.base import TemplateView


__author__ = 'vaio'
from django.conf.urls import patterns, url
from Reservation import views

urlpatterns = patterns('',
                        url(r'^reserve/(\d+)/$', views.reserve, name="reserve_room"),
                        url(r'ajax/hotelserver/$', views.hotel_server),
                        url(r'ajax/reserve/$', views.ajax_reserve),
                        url(r'pay/reservation/(\d+)/$', views.transaction),
                        url(r'^ajax/search/hotel/$', views.search_hotel),
                        url(r'^ajax/search/room/$', views.search_room),
                        url(r'^cancle/reservation/$', views.cancle_reservation, name="cancel")

                        )