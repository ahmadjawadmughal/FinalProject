from django.urls import path
from user import views

urlpatterns = [
    path("", views.signup_user, name="signup-user"),
    path("login/", views.login_user, name="login-user"),
    path('logout/', views.logout_user, name='logout-user'),
    path("home/", views.home, name='home')


]
