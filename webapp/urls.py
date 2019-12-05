from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^contest/$',views.contest,name='contest'),
    url(r'^ranking/$',views.ranking,name= 'ranking'),
    url(r'^profile/$',views.profile, name='profile'),
    url(r'^showimage/$',views.showimage,name ='showimage'),
]
