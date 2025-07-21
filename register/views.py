from django.contrib.auth import get_user_model, login, logout, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse

User = get_user_model()


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        e_mail = request.POST.get("email")
        password = request.POST.get("password")
        """
        adresse = request.POST.get("address") + " " + \
            request.POST.get("postcode") + " " + request.POST.get("city")
            """
        adresse = request.POST.get("address")
        phone = request.POST.get("phone")
        user = User.objects.create_user(first_name=first_name, last_name=last_name, email=e_mail, password=password,
                                        adresse=adresse, phone=phone)
        assert isinstance(user, object)
        login(request, user)
        return redirect(reverse('homepage'))

    return render(request, "register/index.html")


def login_user(request):
    if request.method == "POST":
        e_mail = request.POST.get("email")
        password = request.POST.get("password")
        assert isinstance(password, object)
        user = authenticate(username=e_mail, password=password)
        if user:
            login(request, user)
            return redirect(reverse('homepage'))
    return render(request, "register/login.html")


def logout_user(request):
    logout(request)
    return redirect(reverse('homepage'))


def edit_profile(request):
    if request.method == "POST":
        e_mail = request.POST.get("email")
        password = request.POST.get("password")
        adresse = request.POST.get("address")
        phone = request.POST.get("phone")
        user = request.user
        user.email = e_mail
        user.password = password
        user.adresse = adresse
        user.phone = phone
        user.save()
        return redirect(reverse('homepage'))

    return render(request, "register/update.html")
