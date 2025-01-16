from django.urls import path
from post import views

urlpatterns = [
    path("create/post/", views.create_post, name="create-post"),
    path("update/post/<int:id>/", views.update_post, name="update-post"),
    path("delete/post/<int:id>/", views.delete_post, name="delete-post"),
    path("list/post/", views.list_post, name="list-post"),


]
