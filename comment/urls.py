from django.urls import path
from . import views

urlpatterns = [
    path("detail/<int:id>/", views.detail_post, name="detail-post"),
    path("edit/<int:id>/", views.edit_comment, name="edit-comment"),
    path("delete/<int:id>/", views.delete_comment, name="delete-comment"),
    

]
