from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<title>", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newEntry", views.newEntry, name="newEntry"),
    path("editEntry/<title>", views.edit, name="edit")
]
