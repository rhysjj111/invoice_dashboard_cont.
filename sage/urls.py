from django.urls import path
from . import views

urlpatterns = [
    path('sage_auth', views.sage_auth, name='sage_auth'),
    path('test', views.test, name='test'),
    path('sage_callback', views.sage_callback, name='sage_callback'),
    path('make_api_request', views.make_api_request, name='make_api_request'),
]
