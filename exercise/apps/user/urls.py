from django.conf.urls import url
from user import views
from user.views import Register,Active,Login,ProductionShow,Logout,AddressView
from django.contrib.auth.decorators import login_required



urlpatterns = [
    # url(r'^register$',views.register,name='register'),
    # url(r'^register_handler$',views.register_handle)
    url(r'register',Register.as_view(),name='register'),
    url(r'^active/(?P<active_info>.*)',Active.as_view(),name='active'),
    url(r'login',Login.as_view(),name='login'),
    url(r'production',login_required(ProductionShow.as_view()),name='production'),
    # url(r'production', ProductionShow.as_view(), name='production'),
    url(r"logout",Logout.as_view(),name='logout'),
    url(r'address',AddressView.as_view(),name='address')

]
