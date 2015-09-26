
from django.views.generic.base import TemplateView
import Reservation
from Simorgh import settings

__author__ = 'vaio'

from django.conf.urls import patterns, url
from Manage import views

urlpatterns = patterns('', url(r'^register/$', views.register),
                        url(r'^profile/activate/([A-Z0-9]+)/$', views.activate_account),
                        url(r'^profile/edit/$', views.edit_profile),
                        url(r'^profile/hotel/(\d+)/$', views.hotel_profile, name="hotel_profile"),
                        url(r'^profile/hotels_list/$', views.hotels_list, name="hotels_list"),
                        url(r'^profile/room/(\d+)/$', views.room_profile, name="room_profile"),
                        url(r'^profile/$', views.show_profile, name="profile"),
                        url(r'^login/$', views.my_login, name = "login"),
                        url(r'^logout/$', views.my_logout, name = "logout"),
                        url(r'^forgotpassword/', views.forgot_password, name = "forgotpass"),
                        url(r'^sendusername/', views.send_username, name = "senduser"),
                        url(r'^changepassword/$', views.change_password, name="changepass"),
                        url(r'^add/hotel/$', views.add_hotel, name="add_hotel"),
                        url(r'^add/hotel_photo/(\d+)/$', views.add_hotel_photo),
                        url(r'^remove_photo/$', views.remove_photo),
                        url(r'^add/room/(\d+)/$', views.add_room, name="add_room"),
                        url(r'^add/room_photo/(\d+)/$', views.add_room_photo),
                        url(r'^edit/hotel/(\d+)/$', views.edit_hotel, name="edit_hotel"),
                        url(r'^edit/room/(\d+)/$', views.edit_room, name="edit_room"),
                        url(r'^remove/hotel/$', views.remove_hotel, name="remove_hotel"),
                        url(r'^remove/room/$', views.remove_room, name="remove_room"),
                        url(r'^home/$', TemplateView.as_view(template_name='home.html'), name="home"),
                        url(r'^hotelsList/$', views.show_all_hotels),
                        url(r'^profile/my_comments/$', views.my_comments, name="my_comments"),
                        url(r'^profile/my_reservation/$', views.my_reservation, name="my_reservation"),
                        url(r'^profile/commision/$', views.commision, name="commision" ),
                        url(r'^profile/report/$', views.report, name="report"),
                        url(r'^bank/(\d+)/(\d+)/$', views.bank, name="bank"),
                        url(r'pay/commision/(\d+)/$', views.pay_commision),
                        url(r'pay/reservation/(\d+)/$', views.pay_reservation),
                        url(r'^ajax/hotel/(?P<pk>\d+)/comments$', views.ajax_get_hotel_comments),
                        url(r'^ajax/hotel/(?P<pk>\d+)/comments/add$', views.ajax_add_hotel_comment),
                        url(r'^ajax/income_chart/$', views.chart_month_income),
                        url(r'^ajax/reserve_chart/$', views.chart_month_reserve),
                        url(r'^aboutUs/$', TemplateView.as_view(template_name='aboutUs.html'), name="about"),
                        url(r'^contactUs/$', TemplateView.as_view(template_name='contactUs.html'), name="contact"),
                        url(r'^ajax/home/$', views.ajax_home),
                        )


