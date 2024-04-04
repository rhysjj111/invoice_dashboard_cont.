from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.landing_page, name='landing_page'),
    path('payment/<slug:slug>', views.payment, name='payment'),
    # path('create_checkout_session', views.payment, name='payment'),
    # path('payment_success/<slug:slug>', views.checkout, name='payment_success'),
    # path('payment_declined/<slug:slug>', views.checkout, name='payment_declined'),
    path('create-checkout-session/<slug:slug>', views.create_checkout_session, name='create_checkout_session'),
    path('session-status/', views.session_status, name='session_status'),
    path('return/', views.checkout_return, name='checkout_return'),
    # path('checkout-cancel/', views.checkout_cancel, name='checkout_cancel'),
]
