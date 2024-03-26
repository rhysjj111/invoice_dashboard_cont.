from django.urls import path
from . import views

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('invoice/<slug:slug>', views.invoice_summary, name='invoice'),
    path('create_invoice', views.create_invoice, name='create_invoice'),
]
