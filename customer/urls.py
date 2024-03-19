from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customer', views.customer_summary, name='customer'),
    path('add/', views.add_customer, name='add_customer'),
]
