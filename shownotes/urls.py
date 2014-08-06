from django.conf.urls import patterns, url
from shownotes import views
from shownotes import api

urlpatterns = patterns(
    '',
    url(r'^$', views.index),
    url(r'^search$', views.search_topics),
    url(r'^topics$', views.topics),
    url(r'^api/topics$', api.topics),
    url(r'^api/search$', api.search),
    url(r'^api/show$', api.show)
)
