from django.conf.urls import url, include
from django.contrib.auth.models import User
from django.contrib import admin


from .views import HomeListView, FabricDetailView, FabricCreateView, \
                   FabricDeleteView, FabricUpdateView, ThemeView


urlpatterns = [
    url(r'^hexcode/(?P<color>.+)/$', ThemeView.as_view(), name="hexcode"),

    url(r'^(?P<pk>\d+)/$', FabricDetailView.as_view(), name="fabric-detail"),

    url(r'^create/$', FabricCreateView.as_view(), name="fabric-create"),
    url(r'^delete/(?P<pk>\d+)/$', FabricDeleteView.as_view(), name="fabric-delete"),
    url(r'^update/(?P<pk>\d+)/$', FabricUpdateView.as_view(), name="fabric-update"),
    url(r'^$', HomeListView.as_view(), name="homepage"),
]
