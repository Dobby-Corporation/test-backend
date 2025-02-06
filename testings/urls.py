from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='tests.index'),
    path('list', views.tests_list, name='tests.list'),
    path('<int:id>/answer', views.answer, name='tests.answer'),
    path('<int:id>/finish', views.finish, name='tests.finish'),
    path('<int:id>/info', views.info, name='tests.info'),
    path('<int:id>/show', views.show, name='tests.show'),
    path('<int:id>/start', views.start, name='tests.start'),
    path('<int:id>/result', views.result, name='tests.result'),
]
