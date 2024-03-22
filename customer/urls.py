from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer_list, name='customer_list'),
    path('customer_summary/<slug:slug>', views.customer_summary, name='customer_summary'),
    path('add/', views.add_customer, name='add_customer'),
    path('edit/<slug:slug>', views.edit_customer, name='edit_customer'),
    path('delete/<slug:slug>', views.delete_customer, name='delete_customer'),
    path('add_vehicle', views.add_vehicle, name='add_vehicle'),
    path('edit_vehicle/<slug:slug>', views.edit_vehicle, name='edit_vehicle'),
    # path('delete_vehicle/<slug:redirect_slug>/<slug:slug>', views.delete_vehicle, name='delete_vehicle'),
]
