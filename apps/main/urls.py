from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register/$', views.register, name="register"), #RR
    url(r'^login/$', views.login, name="login"), #RR
    url(r'^logout$', views.logout, name="logout"),
    url(r'^dashboard/$', views.dashboard, name="dashboard"),
    url(r'^books/add$', views.add, name="add"),
    url(r'^books/create$', views.create, name="create"), # RR submit from 'add' route sends form data to db to creat review
    url(r'^books/(?P<book_id>\d+)$', views.show, name="show"),
    url(r'^reviews/create/(?P<book_id>\d+)$', views.reviews_create, name="reviews_create"),
    url(r'^reviews/delete/(?P<review_id>\d+)$', views.reviews_delete, name="reviews_delete"),
    url(r'^user/(?P<user_id>\d+)$', views.user, name="user"),
]