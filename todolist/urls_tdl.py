from django.urls import path
from . import views
from . import views_class

# post/
urlpatterns = [
    # path("", views.home, name="home"),
    # path("create/", views.create_post, name="post_create"),
    # path("<int:post_id>", views.show_post, name="post_show"),
    # path("<int:post_id>/edit", views.edit_post, name="post_edit"),
    # path("<int:post_id>/delete", views.delete_post, name="post_delete")

#     urls_class

    path("", views_class.Home.as_view(), name="home"),
    path("create/", views_class.CreatePost.as_view(), name="post_create"),
    path("<int:post_id>", views_class.ShowPost.as_view(), name="post_show"),
    path("<int:post_id>/edit", views_class.EditPost.as_view(), name="post_edit"),
    path("<int:post_id>/delete", views_class.DeletePost.as_view(), name="post_delete")
]