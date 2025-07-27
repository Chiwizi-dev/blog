from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.contrib import messages

from .models import Account, UserProfile
from .forms import RegistrationForm, UserProfileForm

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from django.contrib.auth import authenticate, login, logout

from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required


# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect("blog:home")
    
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password"]
            
            user = form.save(commit=False)
            user.set_password(password)
            user.save()

            messages.success(request, 'Registration successful! Please use the link sent to your email to activate your account')

            # CONFIGURE ACTIVATION EMAIL LINK
            current_site = get_current_site(request)
            mail_subject = "Please activate your account"
            message = render_to_string("accounts/account_verification_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
            })

            to_email = user.email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            return redirect("accounts:login")
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegistrationForm()

    context = {"form": form}
    return render(request, "accounts/register.html", context)



def activate(request, uidb64, token):
    if request.user.is_authenticated:
        return redirect("blog:home")
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Congratulation! Your account is activated.")

        return redirect("accounts:login")
    else:
        messages.error(request, "Invalid activation link")
        return redirect("accounts:register")
    


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("blog:home")
        else:
            messages.error(request, "Invalid Login!")
            return render(request, "accounts/login.html")
    else:
        return render(request, "accounts/login.html")
    

def confirm_logout(request):
    if not request.user.is_authenticated:
        return redirect("blog:home")
    return render(request, "accounts/confirm_logout.html")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("blog:home")


# @login_required(login_url="/login/")
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect("blog:home")
    user_obj = request.user
    user_pk = request.user.pk


    userprofile = get_object_or_404(UserProfile, user_id=user_pk)


    context = {"user_pk": user_pk, "userprofile":userprofile, "user_obj": user_obj}
    return render(request, "accounts/dashboard.html", context)