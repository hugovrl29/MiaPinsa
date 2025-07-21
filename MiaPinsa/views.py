from django.shortcuts import render


def index(request):
    return render(request, "MiaPinsa/accueil.html", context={"nom": "Hugo"})


def carte(request):
    return render(request, "MiaPinsa/carte.html")


def contact(request):
    return render(request, "MiaPinsa/contact.html")


def horaires(request):
    return render(request, "MiaPinsa/horaires.html")
