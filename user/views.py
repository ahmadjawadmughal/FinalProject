from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER

# Create your views here.


def signup_user(request): 

    if request.method == "POST":

        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not password1 == password2:
            messages.warning(request, "Your password is not match!")
        else:    
            user = User.objects.create_user(username, email, password1)

            user.first_name = fname
            user.last_name = lname
            user.save()

            """EMAIL functionality"""
            subject = "SignedUp"
            message = f"Dear {user.first_name},\n\nCongrats! You're successfully signed up on 'Posting'.\n\nThank You for joining us.\n\nRegards,\nPosting"
            recipient_list = [user.email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)

            
            messages.success(request, "Congrats! You're successfully signedUp.")

            return redirect("home")
    
    else:
         return redirect("home")


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, "Hurray! You're successfully logged in")
            return redirect("home")
        
        messages.error(request, "Your login attempt failed!")
        return redirect("login-user")
    else:
        return HttpResponse("404-found")
    
def home(request):
    return render(request, "home.html")


def logout_user(request):
    logout(request)
    messages.success(request,"You're successfully loggedOut!")

    return redirect("home")
