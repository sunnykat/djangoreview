from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add$', views.add, name='add'),
    url(r'^book/(?P<b_id>\d+)$', views.book, name='book'),
    url(r'^book$', views.newbook, name='newbook'),
    url(r'^user/(?P<u_id>\d+)$', views.user, name='user'),
    url(r'^review$', views.newreview, name='newreview'),
    url(r'^review/(?P<r_id>\d+)/destroy$', views.removereview, name='removereview'),
    
]
