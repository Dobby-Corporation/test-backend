import jwt
import os

from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse

from .services import check_telegram_authorization
from .models import User

# Create your views here.
def auth(request: HttpRequest):
    pass

def login(request: HttpRequest):
    return render(request, 'login.html')

def profile(request: HttpRequest):
    print(request.user_info)
    return render(request, 'profile.html')

def auth_telegram(request: HttpRequest):
    try:
        auth_data = check_telegram_authorization(request.GET, os.environ['TELEGRAM_BOT_TOKEN'])
    except:
        return HttpResponse(status=400)

    try:
        user = User.objects.get(tg_id=request.GET['id'])
    except User.DoesNotExist:
        user = User(tg_id=request.GET.get('id'))

    user.first_name=auth_data.get('first_name')
    user.last_name=auth_data.get('last_name')
    user.username=auth_data.get('username')
    user.photo_url=auth_data.get('photo_url')
    user.save()

    access_token = jwt.encode({
        'id': user.id,
        'tg_id': user.tg_id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'photo_url': user.photo_url,
    }, os.environ.get('JWT_SECRET'))

    response = redirect('users.profile')
    response.set_cookie('access_token', access_token)
    return response
