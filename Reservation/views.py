from random import  randint
import string
import datetime
from django.db.models.query_utils import Q
from django.http.response import HttpResponse
from django.shortcuts import render
from Manage.models import Hotel, Room, Passenger, Reservation, Transaction
from Manage.views import id_generator
from jdatetime.jalali import JalaliToGregorian
from django.views.decorators.csrf import csrf_exempt
import json

__author__ = 'vaio'

@csrf_exempt
def search_room(request):
    search_data = request.POST
    city = search_data.get('city')
    hotel = search_data.get('hotel')
    cost = search_data.get('cost')
    capacity = search_data.get('capacity')
    min_point = search_data.get('min_point')
    max_point = search_data.get('max_point')
    min_star = search_data.get('min_star')
    max_star = search_data.get('max_star')
    pool = search_data.get('pool')
    breakfast = search_data.get('breakfast')
    cafe = search_data.get('cafe')
    wifi = search_data.get('wifi')
    extra_bed = search_data.get('extra_bed')
    tv = search_data.get('tv')
    kitchen = search_data.get('kitchen')
    sort_field = search_data.get('sort_field')

    print(search_data)
    rooms = Room.objects.all()

    if city:
        rooms = Room.objects.filter(hotel__city=city)
    if hotel:
        condition = Q(hotel__name__contains=hotel)
        rooms = rooms.filter(condition)
    if cost:
        rooms = rooms.filter(cost__lte=cost)
    if capacity:
        rooms = rooms.filter(capacity_gte=capacity)
    if min_point:
        rooms = rooms.filter(hotel__average_star_number__gte=min_point)
    if max_point:
        rooms = rooms.filter(hotel__average_star_number__lte=max_point)
    if min_star:
        rooms = rooms.filter(hotel__star_number__gte=min_star)
    if max_star:
        rooms = rooms.filter(hotel__star_number__lte=max_star)
    if pool=='true':
        rooms = rooms.filter(hotel__pool=pool)
    if breakfast=='true':
        rooms = rooms.filter(hotel__breakfast=breakfast)
    if cafe=='true':
        rooms = rooms.filter(hotel__cafe=cafe)
    if wifi=='true':
        rooms = rooms.filter(hotel__wifi=wifi)
    if extra_bed=='true':
        rooms = rooms.filter(extra_bed=extra_bed)
    if tv=='true':
        rooms = rooms.filter(tv=tv)
    if kitchen=='true':
        rooms = rooms.filter(kitchen=kitchen)
    if sort_field == '1':
        print("doroste")
        rooms = rooms.order_by('hotel__star_number')
    if sort_field == '2':
        print("doroste")
        rooms = rooms.order_by('hotel__average_star_number')

    if sort_field == '3':
        print("doroste")
        rooms = rooms.order_by('cost')

    result = []
    for room in rooms:
        a = {}
        a['hotel_name'] = room.hotel.name
        a['star'] = room.hotel.star_number
        a['point'] = room.hotel.average_star_number
        a['link'] = "/simorgh/profile/room/" + str(room.id)
        if len (room.roomphoto_set.all()) !=0:
            a['img_url'] = room.roomphoto_set.all()[0].photo.url
        else:
            a['img_url']=None

        a['price'] = room.cost
        result.append(a)

    json_response = json.dumps({'obj_list':result, 'result': 1}, ensure_ascii=False )
    return HttpResponse(json_response, content_type="application/json")

@csrf_exempt
def search_hotel(request):
    search_data = request.POST
    city = search_data.get('city')
    hotel = search_data.get('hotel')
    min_point = search_data.get('min_point')
    max_point = search_data.get('max_point')
    min_star = search_data.get('min_star')
    max_star = search_data.get('max_star')
    pool = search_data.get('pool')
    breakfast = search_data.get('breakfast')
    cafe = search_data.get('cafe')
    wifi = search_data.get('wifi')
    sort_field = search_data.get('sort_field')

    print("search data chist? miduni?")
    # print(search_data)
    hotels = Hotel.objects.all()
    if city:
        print(city+" helllllo")
        hotels = hotels.filter(city=city)
    if hotel:
        condition = Q(name__contains=hotel)
        hotels = hotels.filter(condition)
    if min_point:
        hotels = hotels.filter(average_star_number__gte=min_point)
    if max_point:
        hotels = hotels.filter(average_star_number__lte=max_point)
    if min_star:
        hotels = hotels.filter(star_number__gte=min_star)
    if max_star:
        hotels = hotels.filter(star_number__lte=max_star)
    if pool=='true':
        hotels = hotels.filter(pool=pool)
    if breakfast=='true' :
        hotels = hotels.filter(breakfast=breakfast)
    if cafe=='true':
        hotels = hotels.filter(cafe=cafe)
    if wifi=='true':
        hotels = hotels.filter(wifi=wifi)
    print()
    if sort_field == '1':
        print("doroste")
        hotels = hotels.order_by('star_number')
    if sort_field == '2':
        print("doroste")
        hotels = hotels.order_by('average_star_number')

    result = []
    for hotel in hotels:
        a = {}
        a['hotel_name'] = hotel.name
        a['star'] = hotel.star_number
        a['point'] = hotel.average_star_number
        a['link'] = "/simorgh/profile/hotel/" + str(hotel.id)
        if len (hotel.hotelphoto_set.all()) !=0:
            a['img_url'] = hotel.hotelphoto_set.all()[0].photo.url
        else:
            a['img_url']=None
        a['price'] = 0
        result.append(a)

    json_response = json.dumps({'obj_list':result, 'result': 1}, ensure_ascii=False )
    return HttpResponse(json_response, content_type="application/json")





def reserve(request, roomId):

    try:
        room = Room.objects.get(pk=roomId)
        return  render(request, "reserve.html", { "room_id": roomId, 'cost': room.cost})
    except Room.DoesNotExist:
        return HttpResponse("room doesn't exist")


    # g_date = searchData['date'].split('/')
    # date = JalaliToGregorian(int(g_date[0]), int(g_date[1]), int(g_date[2])).getGregorianList()
    # res = ""
    # res += str(int(date[0])) + '-'
    # res += str(int(date[1])) + '-'
    # res += str(int(date[2]))

def hotel_server(request):
    random_number = randint(0, 100)
    return HttpResponse(random_number)


def get_date(date):
    g_date = date.split('/')
    date = JalaliToGregorian(int(g_date[0]), int(g_date[1]), int(g_date[2])).getGregorianList()
    res = ""
    res += str(int(date[0])) + '-'
    res += str(int(date[1])) + '-'
    res += str(int(date[2]))

    return res


def ajax_reserve(request):
    reserve_data = request.GET
    print(reserve_data)
    try:
        print("in the try")
        passenger = Passenger.objects.get(pk=request.user.id)

        room = Room.objects.get(pk=reserve_data.get('roomId', ''))
        reservation = Reservation(room=room, passenger=passenger, total_cost=reserve_data['cost'], start_date=get_date(reserve_data['from_date']), end_date=get_date(reserve_data['to_date']))
        print("reservation")
        reservation.save()
    except Room.DoesNotExist:
        return HttpResponse(0)
    return HttpResponse(reservation.id)

def transaction(request, reserveId):
    try:
        reserve_ = Reservation.objects.get(pk=reserveId)
        if reserve_.status == 1:
            return HttpResponse("پرداخت قبلا صورت گرفته است")
        else:
            transaction_ = Transaction(reservation=reserve_, refrence_number=int(id_generator(7, chars=string.digits)))
            transaction_.save()
            return HttpResponse("پرداخت شما با موفقیت انجام شد")
    except Reservation.DoesNotExist:
        return HttpResponse("فرم رزرو با مشخصات داده شده یافت نشد.")



def cancle_reservation(request):
    print("man injam! :|")
    try:
        reserveID = request.GET.get('reserve_id')
        reservation = Reservation.objects.get(pk=reserveID)
        reservation.delete()
        return HttpResponse(1)
    except reservation.DoesNotExist:
        return HttpResponse(0)

