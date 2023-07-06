from django.shortcuts import render, HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out

User = get_user_model()
# Create your views here.


def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        mail = request.POST["mail"]
        uname = request.POST["username"]
        passs = ""
        if request.POST["password"] == request.POST["cnfpassword"]:
            passs = request.POST["password"]

        fullname0 = request.POST["fullname"].strip().split(" ")

        firstname = fullname0[0]
        lastname = fullname0[-1]

        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            email=mail,
            username=uname,
            password=passs,
        )
        user.save()
        print("save")

    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_in(request, user)
            return render(request, "index.html")
    return render(request, "login.html")


def logout(request):
    auth_out(request)
    return render(request, "login.html")
