from django.urls import path
from . import views
from django.contrib.auth.models import User
from django.contrib import admin

urlpatterns = [
    path('index/',views.index, name='index'),
    path('booking/<int:rm_id>/',views.booking, name='booking'),
    path('edit/<int:rm_id>/',views.edit, name='edit'),
    path('add/',views.add, name='add'),
    path('accept/<int:rm_id>/',views.accept, name='accept'),
    path('delete/<int:rm_id>/',views.delete, name='delete'),
    path('bookinglist/',views.bookinglist, name='bookinglist'),
]
