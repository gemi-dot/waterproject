from django.urls import path
from . import views

urlpatterns = [
    path('subscribers/add/', views.add_subscriber, name='add_subscriber'),
    path('subscribers/', views.subscriber_list, name='subscriber_list'),

    path('subscribers/edit/<int:pk>/', views.edit_subscriber, name='edit_subscriber'),

    path('subscribers/delete/<int:pk>/', views.delete_subscriber, name='delete_subscriber'),  # ✅ NEW


    
    path('bills/add/', views.add_water_bill, name='add_water_bill'),
    path('bills/', views.waterbill_list, name='waterbill_list'),
]
