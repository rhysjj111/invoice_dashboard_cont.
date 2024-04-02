from django.urls import path
from . import views

urlpatterns = [
    path('invoice_list', views.invoice_list, name='invoice_list'),
    path('invoice_select/<slug:slug>', views.invoice_summary, name='invoice_summary'),
    path('create_invoice', views.create_invoice, name='create_invoice'),
    path('edit_invoice/<slug:slug>', views.edit_invoice, name='edit_invoice'),
]
