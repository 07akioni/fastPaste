from django.conf.urls import url
from django.contrib import admin
from homePage import views

urlpatterns = [
    url(r'^(?P<hash_str>[0-9]+)$', views.clipBoard),
	url(r'^new/$', views.new_clipboard),
	url(r'^get/$', views.get_clipboard),
	url(r'^save/$', views.save_clipboard),
]
