from django.urls import path
from . import views

from .views import grouped_ledger_view

urlpatterns = [

    path('', views.home, name='home'),  # ← this is what was missing

    
    path('subscribers/add/', views.add_subscriber, name='add_subscriber'),
    path('subscribers/', views.subscriber_list, name='subscriber_list'),
    path('subscribers/edit/<int:pk>/', views.edit_subscriber, name='edit_subscriber'),
    path('subscribers/delete/<int:pk>/', views.delete_subscriber, name='delete_subscriber'),  # ✅ NEW

    path('bills/', views.waterbill_list, name='waterbill_list'),
    path('bills/add/', views.add_water_bill, name='add_water_bill'),
    path('bills/<int:pk>/edit/', views.edit_water_bill, name='edit_water_bill'),  # <-- Must exist!
    path('bills/<int:pk>/delete/', views.delete_water_bill, name='delete_water_bill'),


 
    path('ledger/', views.ledger_list, name='ledger_list'),
    path('ledger/add/', views.add_ledger_entry, name='add_ledger_entry'),
    path('ledger/<int:subscriber_id>/', views.subscriber_ledger, name='subscriber_ledger'),
    path('ledger/grouped/', views.grouped_ledger, name='grouped_ledger'),

 
    path('grouped-ledger/', grouped_ledger_view, name='grouped_ledger'),





]
