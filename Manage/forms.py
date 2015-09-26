__author__ = 'vaio'
from django import forms
from Manage.models import *


class RegisterForm(forms.ModelForm):
    pass_conf = forms.CharField(max_length=50, label="تکرار گذرواژه", widget=forms.PasswordInput)
    isHotelier = forms.BooleanField(label="ثبت نام به عنوان هتل دار", required=False)
    # captcha = CaptchaField()
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        _password = cleaned_data.get('password')
        _pass_conf = cleaned_data.get('pass_conf')

        if _pass_conf and _password and _pass_conf != _password:
            print("validation error")
            raise forms.ValidationError('تکرار کلمه عبور نادرست است.')
        return cleaned_data


    class Meta:
        model = Guest
        fields = ('username', 'password', 'pass_conf', 'first_name', 'last_name', 'gender', 'email',
                  'first_phone', 'second_phone', 'cell_phone', 'isHotelier')
        widgets = {
            'password': forms.PasswordInput,
        }

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ('first_name', 'last_name', 'gender', 'email', 'first_phone', 'second_phone','cell_phone')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='نام کاربری')
    password = forms.CharField(widget=forms.PasswordInput, label='گذرواژه')



    #
    # name = models.CharField("نام", max_length=20)
    # hotelier = models.ForeignKey(Manage, verbose_name="هتل دار")
    # star_number = models.IntegerField("ستاره", max_length=1, choices=star_numbers)
    # average_star_number = models.IntegerField("میانگین ستاره", default=0)
    # critic_number = models.IntegerField("تعداد نظردهندگان", default=0)
    # grade = models.IntegerField("رتبه در رده بندی", default=0)
    # credit_number = models.IntegerField("شماره حساب", blank=False)
    # address = models.TextField("آدرس", max_length=200, bland=False)


class HotelForm(forms.ModelForm):

    class Meta:
        model = Hotel
        fields = ('name', 'star_number', 'credit_number', 'address', 'city', 'phone_number', 'pool','sport', 'lake', 'breakfast', 'wifi', 'cafe', 'parking')

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('cost', 'area', 'type', 'king_bed', 'queen_bed', 'tv', 'wifi', 'kitchen', 'extra_bed')


class HotelPhotoForm(forms.ModelForm):

    class Meta:
        model = HotelPhoto
        fields = ('photo',)

class RoomPhotoForm(forms.ModelForm):

    class Meta:
        model = RoomPhoto
        fields = ('photo',)

class HotelComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields=('text', 'star_number')

class ForgotForm(forms.Form):
    username = forms.CharField(label="نام کاربری", max_length=200)

class ChangePassword(forms.Form):

    last_pass = forms.CharField(max_length=200, widget=forms.PasswordInput, label='گذرواژه قبلی')
    new_pass = forms.CharField(max_length=200, widget=forms.PasswordInput, label='گذر واژه جدید')
    pass_conf = forms.CharField(max_length=200, widget=forms.PasswordInput, label= 'تایید گذرواژه')

    def __init__(self, *args, **kwargs):
        main_username = kwargs.pop("username")
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.user = Guest.objects.get(username=main_username)


    def clean(self):
        cleaned_data = super(ChangePassword, self).clean()

        last_pass = cleaned_data['last_pass']
        new_pass = cleaned_data['new_pass']
        new_pass_conf = cleaned_data['pass_conf']
        if not self.user.check_password(last_pass):
            raise forms.ValidationError("کلمه عبور قبلی اشتباه است.")
        else:
            if new_pass != new_pass_conf:
                raise forms.ValidationError("تکرار کلمه عبور نادرست است.")
        return cleaned_data
