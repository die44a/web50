from django.urls import path, include

from django.shortcuts import redirect

from . import views

urlpatterns = [
    path("wiki/", views.index, name="index"),
    path("", lambda request: redirect('wiki/', permanent=True)), # Redirecting from ""
    path("wiki/pages/<str:name>", views.entry, name="entry"),
    path("wiki/create", views.create, name="create"),
    path("wiki/random", views.randompage, name="randompage"),
    path("wiki/Search", views.search, name="search")
]
