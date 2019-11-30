from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^login/$',views.Login,name= 'Login'),
    url(r'^signup/$',views.signup,name='signup'),
    url(r'^logout/$',views.Logout,name='logout'),
    url(r'^app/',include('webapp.urls'))
]