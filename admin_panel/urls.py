from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='admin-panel.index'),
    path('create-test', views.create_test, name='admin-panel.create-test'),
]
