from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name1>", views.entry1, name="entry1"),
    path("entry2", views.entry2, name="entry2"),
    path("entry3", views.entry3, name="entry3"),
    path("create1", views.create1, name="create1"),
    path("wiki/<str:name1>/create2", views.create2, name="create2")
]
