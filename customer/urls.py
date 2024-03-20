from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customer_summary/<slug:slug>', views.customer_summary, name='customer_summary'),
    path('add/', views.add_customer, name='add_customer'),
    path('edit/<slug:slug>', views.edit_customer, name='edit_customer'),
]
