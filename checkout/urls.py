from django.urls import path
from . import views

urlpatterns = [
    path('<slug:slug>', views.landing_page, name='landing_page'),
    path('payment/<slug:slug>', views.payment, name='payment'),
    path('create-checkout-session/<slug:slug>', views.create_checkout_session, name='create_checkout_session'),
    path('session-status/', views.session_status, name='session_status'),
    path('return/', views.checkout_return, name='checkout_return'),

]
