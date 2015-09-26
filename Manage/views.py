from functools import wraps
import string
import random

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
import json
from django.http.response import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect
from Manage.decorators import hotelier_with_permission, specific_hotelier_only, hoteliers_only
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.utils.timezone import utc

from Manage.forms import EditProfileForm, LoginForm, HotelForm, RoomForm, RegisterForm, HotelPhotoForm, RoomPhotoForm, HotelComment, ForgotForm, ChangePassword, Reservation, Commsion
from Manage.models import Guest, Hotelier, Hotel, Room, Activation, Passenger, HotelPhoto, RoomPhoto, Comment


def check_valid_reservation(reservation):
    if reservation.status == 1:
        return True
    t1 = reservation.request_time
    t2 = datetime.datetime.utcnow().replace(tzinfo=utc)
    delta = t2 - t1
    if delta.total_seconds() > 30 * 60:
        reservation.delete()
        return False
    return True

def send_activation_link(user):
    activation_link = id_generator(20)
    al = Activation(activation_link = activation_link, user_id=user.id)
    al.save()

    url = "http://localhost:8000/simorgh/profile/activate/" + activation_link
    msg = "با سلام"
    msg += "\n"
    msg += "\n"
    if user.gender == "man":
        msg += "آقای "
    else:
        msg += "خانم "
    msg += user.first_name + " " + user.last_name
    msg += "\n"
    msg += "از ثبت نام شما متشکریم. با کلیک بر روی لینک زیر می توانید حساب کاربری خود را فعال سازی کنید."
    msg += "\n"
    msg += "\n"
    msg += url

    subject = "فعال سازی حساب کاربری"
    sender = 'simorgh1393tahlil@gmail.com'
    recipients = [user.email]

    print(recipients[0])
    send_mail(subject, msg, sender, recipients)


def send_password_link(user):
    url = "http://localhost:8000/simorgh/forgotpassword/" + user.username
    msg = "با کلیک بر روی لینک زیر رمز عبور جدید به پست الکترونیکی شما ارسال خواهد شد."
    msg += "\n"
    msg += url

    subject = "فراموشی رمز عبور"

    sender = "simorgh1393tahlil@gmail.com"
    recipients = [user.email]

    send_mail(subject, msg, sender, recipients)


def send_new_password(user):
    new_pass = id_generator(10)
    user.set_password(new_pass)
    user.save()
    msg = "رمز عبور جدید شما:"
    msg += str(new_pass)
    msg += "\n\n"
    msg += "می توانید با مراجعه به لینک زیر رمز عبور خود را تغییر دهید"
    msg += "\n\n"
    msg += "http://localhost/simorgh/profile/changepassword"

    subject = "رمز عبور جدید"

    sender = "simorgh1393tahlil@gmail.com"
    recipients = [user.email]

    send_mail(subject, msg, sender, recipients)


def send_username(request):
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            try:
                my_user = Guest.objects.get(username=username)
                send_password_link(my_user)
                return render(request, "thanks.html", {'message': "لینک تغییر رمز عبور به پست الکترونیکی شما فرستاده شد.", "redir": "/simorgh/home/"})
            except Guest.DoesNotExist:
                return render(request, "thanks.html", {'message': "نام کاربری موجود نمی باشد. لطفا دوباره امتحان کنید.", 'redir': "/simorgh/sendusername/"})
    else:
        form = ForgotForm()
    return render(request, "Login.html", {'form': form, 'value': 'رمز عبور جدید', 'option': 0})


def forgot_password(request, username=""):
    s = str(request.path).split('/')
    try:
        user = Guest.objects.get(username=s[-1])
        send_new_password(user)
        return render(request, "thanks.html", { 'message':'گدرواژه جدید به پست الکترونیکی شما فرستاده شد.', 'redir': '/simorgh/login'})
    except Guest.DoesNotExist:
        return render(request, "thanks.html", {'message':'لینک شما معتبر نمی باشد. لطفا دوباره سعی کنید.', 'redir': '/simorgh/login'})





def change_password(request):
    user = request.user
    username = request.user.username
    if request.method == 'POST':
        form = ChangePassword(request.POST, username = username)
        if form.is_valid():
            user = Guest.objects.get(username=username)
            user.set_password(form.cleaned_data['new_pass'])
            user.save()
            return render(request, "thanks.html", {'message': 'رمز عبور شما تغییر پیدا کرد.','redir': '/simorgh/home/'} )
    else:
        form = ChangePassword(username=username)
    return render(request, 'Login.html', {'form': form, 'value':"تغییر رمز عبور", 'option': 1})



def activate_account(request, activation_url):
    try:
        al = Activation.objects.get(activation_link = activation_url)
        my_user = Guest.objects.get(pk = al.user_id)
        my_user.active = True
        my_user.save()
        al.delete()
    except Activation.DoesNotExist:
        return render(request, 'thanks.html', {'message': "لینک فعالسازی اشتباه است."})

    return render(request, 'thanks.html', {'message': 'حساب شما فعال شد. می توانید وارد شوید.', 'redir': '/simorgh/login'})


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            del form.cleaned_data['pass_conf']
            if form.cleaned_data['isHotelier']:
                del form.cleaned_data['isHotelier']
                user = Hotelier(**(form.cleaned_data))
                user.set_password(form.cleaned_data['password'])
                user.save()
            else:
                del form.cleaned_data['isHotelier']
                user = Passenger(**(form.cleaned_data))
                user.set_password(form.cleaned_data['password'])
                user.save()
            send_activation_link(user)
            return render(request, 'thanks.html', {
                'message': 'از ثبت نام شما متشکریم. برای فعال سازی حساب خود از طریق پست الکترونیکی اقدام کنید.',
            })
    else:
        form = RegisterForm()
    return render(request, "register.html", {'form': form})

@login_required(login_url='/simorgh/login/')
def edit_profile(request):
    username = request.user.username
    user = Guest.objects.get(username=username)
    init = {'username': username, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
            'gender': user.gender,
            'first_phone': user.first_phone, 'second_phone': user.second_phone, 'cell_phone': user.cell_phone,
            }
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.gender = form.cleaned_data['gender']
            user.first_phone = form.cleaned_data['first_phone']
            user.second_phone = form.cleaned_data['second_phone']
            user.cell_phone = form.cleaned_data['cell_phone']
            user.save()
            return render(request, "thanks.html", {'message': 'تغییرات با موفقیت ذخیره شد.', 'redir': '/simorgh/profile/'})
        else:
            print("valid nist")
    else:
        form = EditProfileForm(initial=init)
        return render(request, 'register.html', {'form': form})

def my_login(request):
    if not request.user.is_anonymous:
        logout(request)
    redirect_to = request.REQUEST.get('next', '')
    if not redirect_to:
        redirect_to = "/simorgh/home/"


    # forgetForm = ForgotForm()
    message = ""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            # fahime
            if user is not None:
                my_user = Guest.objects.get(pk = user.id)
                if my_user.active:
                    login(request, user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    form = LoginForm()
                    message = "حساب شما غیر فعال است."
            else:
                form = LoginForm()
                message = "نام کاربری یا گذرواژه شما اشتباه است."
    else:
        form = LoginForm()
    return render(request, "Login.html", {'form': form, 'message': message, 'value':"ورود", 'option': 1})


@login_required(login_url='/simorgh/login/')
def my_logout(request):
    logout(request)
    return HttpResponseRedirect("/simorgh/home")


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_add_hotel")
def add_hotel(request):
    if request.method == "POST":
        form = HotelForm(request.POST)
        if form.is_valid():
            hotel = form.save(commit=False)
            hotel.hotelier_id = request.user.id
            hotel.save()
            return render(request, "thanks.html", {'message': 'هتل شما به ثبت رسید.', 'redir': '/simorgh/profile/hotels_list/'})
    else:
        form = HotelForm()
    return render(request, "hotel/add_hotel.html", {'form': form})

@login_required(login_url='simorgh/login')
def hotels_list(request):
    hotelier_id = request.user.id
    hotelier = Hotelier.objects.get(pk=hotelier_id)
    return render(request, 'hotelier/hotels_list.html', {'hotels':hotelier.hotel_set.all()})


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_add_room")
@specific_hotelier_only
def add_room(request, hotel_id):
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.hotel_id = hotel_id
            room.save()
            return render(request, 'thanks.html', {'message': "اتاق مورد نظر به ثبت رسید", 'redir': '/simorgh/edit/hotel/'+ hotel_id})
    else:
        form = RoomForm()
    return render(request, "hotel/add_room.html", {'form': form})


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_edit_hotel")
@specific_hotelier_only#injaaaaaaaaa
def edit_hotel(request, hotelID):
    try:
        hotel = Hotel.objects.get(pk=hotelID)
        init = {'name': hotel.name, 'hotelier': hotel.hotelier, 'star_number': hotel.star_number,
                'credit_number': hotel.credit_number, 'address': hotel.address, 'city' : hotel.city, 'phone_number' : hotel.phone_number,
                'lake': hotel.lake, 'sport': hotel.sport, 'breakfast': hotel.breakfast, 'wife': hotel.wifi, 'parking': hotel.parking, 'pool': hotel.pool, 'cafe':hotel.cafe}
        if request.method == "POST":
            form = HotelForm(request.POST)
            if form.is_valid():
                hotel.name = form.cleaned_data['name']
                hotel.star_number = form.cleaned_data['star_number']
                hotel.credit_number = form.cleaned_data['credit_number']
                hotel.address = form.cleaned_data['address']
                hotel.city = form.cleaned_data['city']
                hotel.phone_number = form.cleaned_data['phone_number']
                hotel.lake = form.cleaned_data['lake']
                hotel.sport = form.cleaned_data['sport']
                hotel.breakfast = form.cleaned_data['breakfast']
                hotel.pool = form.cleaned_data['pool']
                hotel.parking = form.cleaned_data['parking']
                hotel.cafe = form.cleaned_data['cafe']
                hotel.wifi = form.cleaned_data['wifi']
                hotel.save()
                return render(request, 'thanks.html', {'message': "اطلاعات جدید هتل با موفقیت به ثبت رسید", 'redir': '/simorgh/edit/hotel/'+ hotelID})
        else:
            form = HotelForm(initial=init)
            return render(request, 'hotel/edit.html', {'form': form, 'photoForm': HotelPhotoForm(), 'id': hotel.id, 'type': 'hotel', 'images': hotel.hotelphoto_set.all(), 'rooms': hotel.room_set.all()})
    except Hotel.DoesNotExist:
        return render(request, 'thanks.html', {'message': "هتل مورد نظر وجود ندارد.", 'redir' : '/simorgh/profile/'})


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_edit_hotel")
def add_hotel_photo(request, hotelID):
    try:
        hotel = Hotel.objects.get(pk=hotelID)
        if request.method == "POST":
            form = HotelPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.hotel = hotel
                image.save()
                response = json.dumps({'url': image.photo.url, 'imageId': image.id})
                return HttpResponse(response, content_type="application/json")
        else:
            form = HotelPhotoForm()
        return render(request, 'hotel/edit.html', {'form': form})
    except Hotel.DoesNotExist:
        return render(request, 'thanks.html', {'message': "هتل مورد نظر وجود ندارد.", 'redir' : '/simorgh/profile/'})


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_edit_hotel")
def add_room_photo(request, roomID):
    try:
        print("helllooooo I am hereee")
        room = Room.objects.get(pk=roomID)
        if request.method == "POST":
            form = RoomPhotoForm(request.POST, request.FILES)
            if form.is_valid():
                image = form.save(commit=False)
                image.room = room
                image.save()
                response = json.dumps({'url': image.photo.url, 'imageId': image.id})
                return HttpResponse(response, content_type="application/json")
        else:
            form = RoomPhotoForm()
        return render(request, 'hotel/edit.html', {'form': form})
    except Hotel.DoesNotExist:
        return render(request, 'thanks.html', {'message': "هتل مورد نظر وجود ندارد.", 'redir' : '/simorgh/profile/'})

@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_edit_room")
def remove_photo(request):
    imageId = request.GET.get('imageId')
    type = request.GET.get('type')
    print(request.GET)
    try:
        if type == 'hotel':
            image = HotelPhoto.objects.get(pk=imageId)
        else :
           image = RoomPhoto.objects.get(pk=imageId)
        print(imageId + " " + image.photo.url)
        image.delete()
        return HttpResponse(1)
    except HotelPhoto.DoesNotExist:
        return HttpResponse(0)





@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_edit_room")
def edit_room(request, roomID):
    try:
        room = Room.objects.get(pk=roomID)
        init = {'cost': room.cost, 'area': room.area, 'type': room.type,
                'queen_bed': room.queen_bed, 'king_bed': room.king_bed, 'tv': room.tv, 'wifi':room.wifi, 'kitchen': room.kitchen, 'extra_bed': room.extra_bed}
        if request.method == "POST":
            form = RoomForm(request.POST)
            if form.is_valid():
                room.cost = form.cleaned_data['cost']
                room.area = form.cleaned_data['area']
                room.type = form.cleaned_data['type']
                room.queen_bed = form.cleaned_data['queen_bed']
                room.king_bed = form.cleaned_data['king_bed']
                room.tv = form.cleaned_data['tv']
                room.wifi = form.cleaned_data['wifi']
                room.kitchen = form.cleaned_data['kitchen']
                room.extra_bed = form.cleaned_data['extra_bed']
                room.save()
                return render(request, 'thanks.html', {'message': "اطلاعات جدید اتاق با موفقیت به ثبت رسید.", 'redir': '/simorgh/edit/room/'+ roomID})
        else:
            form = RoomForm(initial=init)
            return render(request, 'hotel/edit.html', {'form': form, 'photoForm': RoomPhotoForm(), 'id': room.id, 'type': 'room', 'images': room.roomphoto_set.all(), 'room': 1})
    except Room.DoesNotExist:
        return render(request, 'thanks.html', {'message': "اتاق مورد نظر وجود ندارد.", 'redir' : '/simorgh/profile/'})


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_delete_hotel")
@specific_hotelier_only#injaaaaaaaaa
def remove_hotel(request):
    try:
        hotelID = request.GET.get('hotel_id')
        hotel = Hotel.objects.get(pk=hotelID)
        hotel.room_set.all().delete()
        name = hotel.name
        hotel.delete()
        return HttpResponse(1)
    except Hotel.DoesNotExist:
        return HttpResponse(0)


@login_required(login_url='/simorgh/login/')
@hotelier_with_permission("can_delete_room")
def remove_room(request):
    try:
        roomID = request.GET.get('room_id')
        room = Room.objects.get(pk=roomID)
        room.delete()
        return HttpResponse(1)
    except Room.DoesNotExist:
        return HttpResponse(0)


def hotel_profile(request, hotel_id):
    access=False
    try:
        passenger_id = request.user.id
        passenger = Passenger.objects.get(pk=passenger_id)
        reserve_list= passenger.reservation_set.all()
        for reserve in reserve_list:
            if reserve.room.hotel.id == int(hotel_id) and reserve.end_date >= datetime.datetime.utcnow().replace(tzinfo=utc):
                access=True
    except:
        access=False
    try:
        hotel = Hotel.objects.get(pk = hotel_id)
        hotelImages = hotel.hotelphoto_set.all()
        rooms = hotel.room_set.all()
        roomImages = []
        for room in rooms:
            roomImages.append(room.roomphoto_set.all())
        return render(request, "hotel/hotel_profile.html", {'rooms': rooms, 'hotelImages': hotelImages, 'roomImages': roomImages, 'hotel':hotel, 'access':access})
    except Hotel.DoesNotExist:
        return render(request, 'thanks.html', {'message': "هتل مورد نظر وجود ندارد.", 'redir' : '/simorgh/home/'})


def show_all_hotels(request) :
    hotels = Hotel.objects.all()
    hotel_list = []
    for hotel in hotels:
        image = hotel.hotelphoto_set.all()[0]
        hotel_list.append((hotel, image))
    return render(request, "hotels.html", {"hotels": hotel_list})

@login_required(login_url='/simorgh/login/')
def room_profile(request, room_id):
    try:
        room = Room.objects.get(pk = room_id)
        return render(request, "hotel/room_profile.html", {'room': room, 'roomImage': room.roomphoto_set.all()})
    except Room.DoesNotExist:
        return render(request, 'thanks.html', {'message': "اتاق مورد نظر وجود ندارد.", 'redir' : '/simorgh/home/'})



@login_required(login_url='/simorgh/login/')
def show_profile(request, *args, **kwargs):
    id = request.user.id
    try:
        hotelier = Hotelier.objects.get(pk=id)
        hotel_set=hotelier.hotel_set.all()
        print("man injaam")
        return render(request, 'hotelier/profile.html' ,{'hotelier':hotelier})

    except Hotelier.DoesNotExist:
        try:
            passenger = Passenger.objects.get(pk=id)
            return render(request, 'passenger/profile.html' ,{'passenger': passenger})
        except Passenger.DoesNotExist:
            redirect("simorgh/login/")


#changed from here
@login_required(login_url='simorgh/login')
#@passenger_only
def my_comments(request):
    passenger_id = request.user.id
    passenger = Passenger.objects.get(pk=passenger_id)
    return render(request, 'passenger/mycomments.html', {'comments':passenger.comment_set.all()})

@login_required(login_url='simorgh/login')
#@passenger_only
def my_reservation(request):
    passenger_id = request.user.id
    passenger = Passenger.objects.get(pk=passenger_id)
    reservations = list(passenger.reservation_set.all())
    for reservation in reservations:
        if check_valid_reservation(reservation) == False:
            reservations.remove(reservation)
    return render(request, 'passenger/myreservation.html', {'reservations':reservations})

@login_required(login_url='simorgh/login')
@hoteliers_only
def commision(request):
    hotelier_id = request.user.id
    hotelier = Hotelier.objects.get(pk=hotelier_id)
    commisions = hotelier.commsion_set.all().order_by('start_date')
    if commisions :
        my_com = commisions.filter(status = False)
        if my_com.count() != 0:
            last_commision = Commsion.objects.get(pk=my_com[0].id)
        else:
            last_commision = None
    else :
        last_commision = None
    return render(request, 'hotelier/commision.html', {'commisions': commisions, 'last_commision': last_commision})


@login_required(login_url='simorgh/login')
@hoteliers_only
def report(request):
    hotelier_id = request.user.id
    hotelier = Hotelier.objects.get(pk=hotelier_id)
    hotels = hotelier.hotel_set.all()
    return render(request, 'hotelier/report.html', {'hotelier':hotelier, 'hotels': hotels})

@login_required(login_url='simorgh/login')
def bank(request, payType, payID):
    if payType == '0':
        payment = Commsion.objects.get(pk=payID).total
        url = '/simorgh/pay/commision/' + str(payID)
        print("bebin injam alan :|")
    else:
        reserve = Reservation.objects.get(pk=payID)
        if check_valid_reservation(reserve) == False:
            return render(request, 'thanks.html', {'message': '۳۰ دقیقه از زمان رزرو گذشته است و رزرو لغو شده است.', 'redir':'/simorgh/profile/my_reservation/'})
        else:
            payment = Reservation.objects.get(pk=payID).total_cost
            url = '/simorgh/pay/reservation/' + str(payID)
    return render(request, 'bank.html', {'payment': payment, 'url': url})

@csrf_exempt
def ajax_add_hotel_comment(request, pk):
    p = Hotel.objects.get(id=pk)
    passenger_id = request.user.id
    passenger = Passenger.objects.get(pk=passenger_id)
    star_num=int(request.POST.get("star", 1) )
    p.average_star_number=(p.average_star_number*p.critic_number+star_num)/(p.critic_number+1)
    p.critic_number+=1
    p.save()
    comment = Comment(passenger=passenger, hotel=p, text=request.POST.get('message', ''), star_number=star_num )
    comment.save()
    response = {
        'result': 1,
        }
    return HttpResponse(json.dumps(response), 'application/javascript')

@csrf_exempt
def ajax_get_hotel_comments(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    p = Hotel.objects.get(id=pk)
    comments = p.comment_set.all()

    response = {
        'result': 1,
        'commentList': [{
                            'message': comment.text,
                            'name': '%s %s' % (comment.passenger.first_name, comment.passenger.last_name),
                            'star_number': comment.star_number
                            } for comment in comments]
    }
    return HttpResponse(json.dumps(response), 'application/javascript')


def pay_commision(request, commisionId):
    commision = Commsion.objects.get(pk=commisionId)
    commision.status = 1
    commision.end_date = datetime.datetime.utcnow().replace(tzinfo=utc)
    commision.save()
    return render(request, 'thanks.html', {
        'message':'کارمزد این ماه شما با موفقیت پرداخت شد.',
        'redir':'/simorgh/profile/commision/'
    })

def pay_reservation(request, reservationId):
    reserve = Reservation.objects.get(pk=reservationId)
    reserve.status = 1
    reserve.save()
    hotelier = Hotel.objects.get(pk = Room.objects.get(pk=reserve.room_id).hotel_id).hotelier

    commisions = hotelier.commsion_set.all()
    if commisions :
        my_com = commisions.filter(status = False)
        if my_com.count() != 0:
            new_com = Commsion.objects.get(pk=my_com[0].id)
            new_com.total = my_com[0].total + (reserve.total_cost * 0.15)
            new_com.save()
        else:
            my_com = Commsion(hotelier=hotelier, total=reserve.total_cost * 0.15)
            my_com.save()
    else :
        my_com = Commsion(hotelier=hotelier, total=reserve.total_cost * 0.15)
        my_com.save()
    return render(request, 'thanks.html', {
        'message':'مبلغ رزرو شما با موفقیت پرداخت شد.',
        'redir':'/simorgh/profile/my_reservation/'
    })

def chart_month_reserve(request):
    hotelId = request.GET.get('hotel_id')
    print(hotelId)
    try:
        hotel = Hotel.objects.get(pk=hotelId)
        rooms = hotel.room_set.all()
        res1= {}
        for i in range(12):
            res1[i] = 0
            for room in rooms:
                reservs = room.reservation_set.filter(start_date__month = i + 1)
                res1[i] += reservs.count()

        res2 = {}
        for room in rooms:
            res2[room.type] = room.reservation_set.all().count()
        print("here")
        return HttpResponse(json.dumps({'res1':res1, 'res2': res2}), 'application/javascript')
    except Hotel.DoesNotExist:
        print("here it is")
        return Http404()


def chart_month_income(request):
    hotelId = request.GET.get('hotel_id')
    try:
        hotel = Hotel.objects.get(pk=hotelId)
        rooms = hotel.room_set.all()

        res = {}
        for i in range(12):
            res[i] = 0
            for room in rooms:
                reserves = room.reservation_set.filter(start_date__month = i + 1)
                for reserve in reserves:
                    res[i] += reserve.total_cost
        return HttpResponse(json.dumps(res), 'application/javascript')
    except Hotel.DoesNotExist:
        return Http404()


@csrf_exempt
def ajax_home(request):

    hotels = Hotel.objects.all()
    if hotels.count() > 6:
        print("helllllllloo")
        print(hotels.count() )
        hotels = hotels[:6]

    res = []
    for hotel in hotels:
        a = {}
        a['hotel_name'] = hotel.name
        a['star'] = hotel.star_number
        a['point'] = hotel.average_star_number
        a['link'] = "/simorgh/profile/hotel/" + str(hotel.id)
        if hotel.hotelphoto_set.count() > 0:
            a['img_url'] = hotel.hotelphoto_set.all()[0].photo.url
        else:
            a['img_url'] = ''
        a['price'] = 0
        res.append(a)

    return HttpResponse(json.dumps({'result': 1, "obj_list": res}))

