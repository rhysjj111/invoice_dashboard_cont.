from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.landing_page, name='landing_page'),
    path('payment/<slug:slug>', views.payment, name='payment'),
    # path('payment_success/<slug:slug>', views.checkout, name='payment_success'),
    # path('payment_declined/<slug:slug>', views.checkout, name='payment_declined'),
]
