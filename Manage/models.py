from django.contrib.auth.models import User, AbstractUser
from django.db import models

# Create your models here.
from django.db.models.base import Model

star_numbers = (
        (0, "بدون ستاره"),
        (1, "یک ستاره"),
        (2, "دو ستاره"),
        (3, "سه ستاره"),
        (4, "چهار ستاره"),
        (5, "پنج ستاره")
    )

class Guest(User):
    gender = models.CharField("جنسیت", max_length=10, choices=[("man", "مرد"), ("women", "زن")])
    first_phone = models.IntegerField("تلفن ثابت", max_length=15)
    second_phone = models.IntegerField("تلفن جایگزین", max_length=15)
    cell_phone = models.IntegerField("تلفن همراه", max_length=15)
    active = models.BooleanField("فعال شده", default=False)





class Hotelier(Guest):
    #TODO: this is a sample permission, add relevant permissions later
    can_edit_hotel = models.BooleanField(default=False)
    can_edit_room = models.BooleanField(default=False)
    can_delete_hotel = models.BooleanField(default=False)
    can_delete_room = models.BooleanField(default=False)
    can_add_room= models.BooleanField(default=False)
    can_add_hotel= models.BooleanField(default=True)
    can_add_hotel= models.BooleanField(default=False)


    def __str__(self):
        return str(self.first_name)

    class Meta:
        verbose_name = "هتل دار"
        verbose_name_plural = "هتل داران"

class Commsion(models.Model):
    hotelier = models.ForeignKey(Hotelier, verbose_name="هتل دار")
    total = models.BigIntegerField('مبلغ', default=0)
    start_date = models.DateField("از تاریخ", auto_now=True)
    end_date = models.DateField("تا تاریخ", auto_now=True)
    status = models.BooleanField("وضعیت پرداخت", default=False)


    class Meta:
        verbose_name = "کارمزد"
        verbose_name_plural = "کارمزدها"


class Hotel(models.Model) :
    name = models.CharField("نام", max_length=20)
    hotelier = models.ForeignKey(Hotelier, verbose_name="هتل دار")
    star_number = models.IntegerField("ستاره", max_length=1, choices=star_numbers)
    average_star_number = models.FloatField("میانگین ستاره", default=0)
    critic_number = models.IntegerField("تعداد نظردهندگان", default=0)
    grade = models.IntegerField("رتبه در رده بندی", default=0)
    credit_number = models.IntegerField("شماره حساب", blank=False)
    address = models.TextField("آدرس", max_length=200, blank=False)
    city = models.CharField("شهر", max_length=20)
    phone_number = models.BigIntegerField("شماره تلفن")
    lake = models.BooleanField("منظره ساحل")
    pool = models.BooleanField(" استخر")
    sport = models.BooleanField("امکانات ورزشی")
    breakfast = models.BooleanField("صبحانه")
    wifi = models.BooleanField("اینترنت در لابی")
    parking = models.BooleanField("پارکینگ")
    cafe = models.BooleanField("کافه رستوران")


    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = "هتل"
        verbose_name_plural = "هتل ها"


class HotelPhoto(models.Model):
    photo = models.ImageField("عکس",upload_to=r"photo\hotelphotos")
    hotel = models.ForeignKey(Hotel, verbose_name="هتل")

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, verbose_name="هتل")
    type = models.CharField("نوع", max_length=20)
    cost = models.BigIntegerField("قیمت روزانه")
    area = models.IntegerField("متراژ")
    king_bed = models.IntegerField("تخت دونفره")
    queen_bed = models.IntegerField("تخت یک نفره")
    tv = models.BooleanField("تلویزیون")
    wifi = models.BooleanField("اینترنت")
    kitchen = models.BooleanField("آشپزخانه")
    extra_bed = models.BooleanField("تخت سفری")

    def __str__(self):
        return str( "هتل " +self.hotel.name + ": اتاق " + self.type)

    class Meta:
        verbose_name = "اتاق"
        verbose_name_plural = "اتاق ها"



class RoomPhoto(models.Model):
    room = models.ForeignKey(Room, verbose_name="اتاق")
    photo = models.ImageField("عکس", upload_to=r"photo\roomphotos")



class Passenger(Guest):
    room = models.ManyToManyField(Room, verbose_name="اتاق", through="Reservation")

    def __str__(self):
        return str(self.first_name)

    class Meta:
        verbose_name = "مسافر"
        verbose_name_plural = "مسافران"


class Reservation(models.Model):
    passenger = models.ForeignKey(Passenger, verbose_name="مسافر")
    room = models.ForeignKey(Room, verbose_name="اتاق")
    start_date = models.DateField("تاریخ شروع")
    end_date = models.DateField("تاریخ پایان")
    request_time = models.DateTimeField("زمان درخواست", auto_now=True)
    total_cost = models.BigIntegerField("هزینه کل")
    status_choices = (
        (1, "پرداخت شده"),
        (0, "پرداخت نشده"),

    )
    status = models.IntegerField("وضعیت درخواست", default=0)

    def __str__(self):
        return self.room.type + ": " + str(self.passenger)

    class Meta:
        verbose_name = "درخواست رزرو"
        verbose_name_plural = "درخواست های رزرو"


class Transaction(models.Model):
    reservation = models.OneToOneField(Reservation, verbose_name="درخواست رزرو")
    refrence_number = models.IntegerField("شماره پیگیری", max_length=7)

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش ها"


class Comment(models.Model):
    passenger = models.ForeignKey(Passenger, verbose_name="مسافر")
    hotel = models.ForeignKey(Hotel, verbose_name="هتل")
    text = models.TextField("متن نظر")
    star_number = models.IntegerField(choices=star_numbers, max_length=1)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
            return '%s: %s' % (self.passenger.first_name, self.text)



class Activation(models.Model):
    activation_link = models.CharField("لینک فعال سازی", max_length=20)
    user_id = models.IntegerField("شناسه کاربر")


