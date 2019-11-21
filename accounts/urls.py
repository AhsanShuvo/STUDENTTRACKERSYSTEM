from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login, name='login'),
    path('',views.index, name='index'),
    path('home',views.home, name='home'),
    path('signup',views.signup, name='signup'),
]
