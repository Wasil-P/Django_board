from django.urls import path
from todolist import views_class

urlpatterns = [
    path("", views_class.ShowProfile.as_view(), name="profile_show"),
    path("edit/", views_class.EditProfile.as_view(), name="edit_user"),
]
