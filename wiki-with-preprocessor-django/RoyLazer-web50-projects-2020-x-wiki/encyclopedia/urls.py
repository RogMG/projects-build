from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("newpage", views.createPage, name="newpage"),
    path("randomize", views.randomize, name="randomize"),
    path("edit/<str:title>", views.editpage, name="editpage"),
    path("search", views.searchq, name="search")  
    ]
