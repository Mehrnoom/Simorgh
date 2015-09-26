from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Manage.models import Hotelier, Hotel

__author__ = 'vaio'

def hoteliers_only(view):
    """
    Make sure the view is only visible to Hoteliers
    """
    def new_view(request, *args, **kwargs):
        response = view(request, *args, **kwargs)
        id = request.user.id
        my_user = Hotelier.objects.get(pk=id)
        if my_user != None:
            return response
        # TODO: Add your own forbidden view
        return render(request, 'thanks.html', {'message': 'شما مجاز به انجام این تغییرات نیستید.', 'redir' : '/simorgh/home/'})

    return new_view

def specific_hotelier_only(view):
    """
    Make sure the view is only visible to Hoteliers
    """
    def new_view(request, hotel_id):
        id = request.user.id
        try:
            hotelier = Hotel.objects.get(pk=hotel_id).hotelier_id
            if hotelier != id:
                return render(request, 'thanks.html', {'message': 'شما مجاز به انجام این تغییرات نیستید.', 'redir' : '/simorgh/profile/'})
            else:
                return view(request, hotel_id);
        except Hotel.DoesNotExist:
                return render(request, 'thanks.html', {'message': 'هتل مورد نظر وجود ندار', 'redir' : '/simorgh/home/'})

    return new_view


def hotelier_with_permission(permission_str):
    """
    Make sure the view is only visible to Hoteliers that have permission_str permission
    """
    print("antape3")
    def dec(view):
        print("antape2:))")
        def new_view(request, *args, **kwargs):
            id = request.user.id
            try:
                my_user = Hotelier.objects.get(pk=id)
                if getattr(my_user, permission_str) == True:
                    return view(request, *args, **kwargs)
                # TODO: Add your own forbidden view
                return render(request, 'thanks.html', {
                    'message': 'شما مجاز به انجام این تغییرات نیستید.',
                    'redir' : '/simorgh/home/'
                })

            except Hotelier.DoesNotExist:
                return render(request, 'thanks.html', {
                    'message': 'شما مجاز به انجام این تغییرات نیستید.',
                    'redir' : '/simorgh/home/'
                })
        return new_view

    return dec

