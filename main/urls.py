from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('',views.index,name='index'),
    path('movies/<int:id>',views.movies,name='movies'),
    path('seat/<int:id>',views.seat,name='seat'),
     path('initiate-booking/', views.initiate_booking, name='initiate_booking'),
    path('payment-success/', views.payment_success, name='payment_success'),
    
    path('booked',views.booked,name='booked'),
    path('ticket/<int:id>',views.ticket,name='ticket'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)