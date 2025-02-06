from django.urls import path

from . import views

urlpatterns = [
    path('<uuid:file_uuid>', views.get_file, name='files.get'),
]
