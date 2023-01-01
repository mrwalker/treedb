from django.urls import path

from . import views

app_name = 'trees'
urlpatterns = [
    path('', views.index, name='index'),
    path('json/', views.index_json, name='index_json'),
    path('<int:tree_id>/', views.detail, name='detail'),
    path('<int:tree_id>/qrcode/', views.qrcode, name='qrcode'),
]
