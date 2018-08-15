from django.conf.urls import url
from apps.production.views import Index,Detail,ShowAllCar

urlpatterns = [
    url(r'^$',Index.as_view(),name='index'),
    url(r'^detail/(?P<c_id>\d+)$',Detail.as_view(),name='detail'),
    url(r'^show/(?P<b_id>\d+)/(?P<page>\d+)',ShowAllCar.as_view(),name='showcar')

]
