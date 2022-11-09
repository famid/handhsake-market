from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages


def register_request(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in!!")
        return redirect(to="market_page")

    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}")

            return redirect(to="login")
        else:
            messages.error(request, form.errors)

    template_name = "user_auth/register.html"
    form = NewUserForm()
    return render(request, template_name, context={"form": form})


def login_request(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in!!")
        return redirect(to="market_page")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_staff:
                    return redirect(to="user_list")

                return redirect(to="market_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    template_name = "user_auth/login.html"
    form = AuthenticationForm()
    return render(request, template_name, context={"login_form": form})


@login_required
def custom_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")

    return redirect("login")
