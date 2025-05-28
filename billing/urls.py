from django.urls import path
from . import views

urlpatterns = [
    path('subscribers/add/', views.add_subscriber, name='add_subscriber'),
    path('subscribers/', views.subscriber_list, name='subscriber_list'),

    
    path('bills/add/', views.add_water_bill, name='add_water_bill'),
    path('bills/', views.waterbill_list, name='waterbill_list'),
]
