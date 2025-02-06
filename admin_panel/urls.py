from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='admin-panel.index'),
    path('test/new', views.create_test, name='admin-panel.create-test'),
    path('test/<int:id>/edit', views.edit_test, name='admin-panel.edit-test'),
    path('test/<int:id>/results', views.get_test_results, name='admin-panel.test-results'),
    path('test/<int:id>/details', views.get_test_result_details, name='admin-panel.test-result-details'),
]
