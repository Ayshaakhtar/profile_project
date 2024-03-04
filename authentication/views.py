import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout,authenticate
from django.template import RequestContext
from.models import Profile
from django.core.mail import BadHeaderError,send_mail
from django.conf import settings

def login_user(request):
    if request.method == 'POST':
        #email = request.POST.get('email')
        username = request.POST.get('name')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("Home")
    else:
        return render(request, 'authentication/login.html')




# Create your views here.


def registration_user(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        password1 = request.POST.get("password1")

        if User.objects.filter(username=name).exists():
            messages.error(request, 'Username is already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
        elif password != password1:
            messages.error(request, 'Passwords do not match.')
        else:
            # Create the user
            user = User.objects.create_user(username=name, email=email, password=password)
            user.set_password(password)
            user.save()
            otp = random.randint(0000,9999)
            prof = Profile(user=user, token=otp)
            prof.save()
            subject = "Your account verification code"
            message = f'Hi here is your account verification otp : {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient = [email]
            send_mail(subject, message, from_email, recipient)
            messages.success(request, "Account created please check email to varify")
            return redirect("verify_acc")
    else:
        return render(request, 'authentication/registration.html')


def logout_user(request):
    logout(request)
    return redirect(login)

def verify_acc(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        prof = Profile.objects.get(token=otp)
        if prof:
            prof.is_verified = True
            prof.save()
            messages.success(request, "Profile successfully verified")
            return redirect('login_user')
        else:
            messages.success(request, "wrong otp")
            return redirect('verify_acc')

    return render(request, "authentication/verify.html")
