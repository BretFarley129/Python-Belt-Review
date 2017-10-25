from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^books/newBook$', views.newBook),
    url(r'^books/(?P<number>\d+)$', views.showbook),
    url(r'^delete/(?P<number>\d+)/(?P<boo>\d+)$', views.delete),
    url(r'^books/(?P<number>\d+)/new$', views.new),
    url(r'^users/(?P<number>\d+)$', views.showuser),
]