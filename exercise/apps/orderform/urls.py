from django.conf.urls import url

from apps.orderform.views import*
urlpatterns = [
 url(r'^create',Create.as_view,name='create'),
 url(r'showorder',ShowOrder,name='show'),
 url(r'commit',Commit.as_view,name='commit'),
 url(r'cost', Cost.as_view, name='cost'),
url(r'check', Check.as_view, name='check'),
]
