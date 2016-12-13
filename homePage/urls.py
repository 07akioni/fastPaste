from django.conf.urls import url
from django.contrib import admin
from homePage import views

urlpatterns = [
    url(r'^(?P<hash_str>[0-9]*)$', views.clipBoard),
	url(r'^new/$', views.new_clipboard),
	url(r'^get/(?P<hash_str>[0-9]+)$', views.get_clipboard),
	url(r'^post/$', views.post_clipboard),
	url(r'^[^\s]*$', views.not_found),
]
