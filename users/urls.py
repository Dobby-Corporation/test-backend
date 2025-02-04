from django.urls import path

from . import views

urlpatterns = [
    path('auth', views.auth, name='users.auth'),
    path('auth/telegram', views.auth_telegram, name='users.auth.telegram'),
    path('profile', views.profile, name='users.profile'),
    path('login', views.login, name='users.login'),
]
