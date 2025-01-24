from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from mysite.settings import EMAIL_HOST_USER
from .forms import SignupForm
from post.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

"""
def signup_user(request): 

    if request.method == "POST":

        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

       
        if not password1 == password2:
            messages.warning(request, "Your password does not match!")
        else:    
            user = User.objects.create_user(username, email, password1)

            user.first_name = fname
            user.last_name = lname
            user.save()

            #EMAIL functionality
            subject = "SignedUp"
            message = f"Dear {user.first_name},\n\nCongrats! You're successfully signed up on 'Posting'.\n\nThank You for joining us.\n\nRegards,\nPosting"
            recipient_list = [user.email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)

            
            messages.success(request, "Congrats! You're successfully signedUp.")

            return redirect("home")
    return render(request, "signup.html")
"""


def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # Authenticate the user
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in
            login(request, user)
            messages.success(request, f"{user.username}! You're successfully logged in")
            return redirect("home")
        
        messages.error(request, "Your login credentials failed!")
        return redirect("login-user")
    return render(request,"login.html")


def signup_user(request): 
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save to database yet
            user.set_password(form.cleaned_data["password"])  # Hash the password
            user.save()

            """EMAIL functionality"""
            subject = "Signed Up"
            message = (
                f"Dear {user.first_name},\n\n"
                f"Congrats! You're successfully signed up on 'Posting'.\n\n"
                "Thank you for joining us.\n\n"
                "Regards,\nPosting"
            )
            recipient_list = [user.email]
            send_mail(subject, message, EMAIL_HOST_USER, recipient_list, fail_silently=True)

            messages.success(request, "Congrats! You're successfully signed up.")
            return redirect("login-user")
        else:
            # Form is invalid, display detailed errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = SignupForm()  # An empty form for GET requests

    return render(request, "signup.html", {"form": form})




def home(request):
    return render(request, "home.html")






@login_required
def logout_user(request):
    user = request.user
    logout(request)
    messages.success(request,f"{user.username} successfully loggedOut!")

    return redirect("login-user")



