from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out
from .models import Book

User = get_user_model()
# Create your views here.


def home(request):
    return render(request, "index.html")


def signup(request):
    if request.method == "POST":
        mail = request.POST['mail']
        print(mail)
        username = request.POST['username']
        print(username)
        password = request.POST['password']
        print(password)
        # cnfpassword = request.POST['cnfpassword']
        # print(cnfpassword)
        # # fullname = request.POST['fullname']
        fullname = request.POST["fullname"].strip().split(" ")
        print(fullname)
        # gender = request.POST.get('gender', False)
        # print(gender)
        # city = request.POST['city']
        # print(city)
        # state = request.POST['state']
        # print(state)
        # card_type = request.POST['card_type']
        # print(card_type)
        # credit_card_no = request.POST['credit_card_no']
        # print(credit_card_no)
        # cvc = request.POST['cvc']
        # print(cvc)
        # exp_month = request.POST['exp_month']
        # print(exp_month)
        # exp_year = request.POST['exp_year']
        # print(exp_year)

        user = User.objects.create_user(username, mail, password)
        user.first_name = fullname[0]
        user.last_name = fullname[-1]
        user.public_visibility = True
        user.save()
        print('save')

        # mail = request.POST["mail"]
        # uname = request.POST["username"]
        # passs = ""
        # if request.POST["password"] == request.POST["cnfpassword"]:
        #     passs = request.POST["password"]

        # fullname0 = request.POST["fullname"].strip().split(" ")

        # firstname = fullname0[0]
        # lastname = fullname0[-1]

        # user = User.objects.create_user(
        #     first_name=firstname,
        #     last_name=lastname,
        #     email=mail,
        #     username=uname,
        #     password=passs,
        # )
        # user.save()
        # print("save")

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
    return redirect('login')

def author_and_sellers(request):
    # authors_sellers
    data = User.objects.filter(public_visibility=True, is_superuser=False)
    return render(request, 'basic-table.html', {'authors_sellers': data})

def bookupload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            cover_img = request.FILES['coverimg']
            book = request.FILES['book']
            price = int(request.POST['price'])
            data_save = Book()
            data_save.username = request.user
            data_save.title = title
            data_save.coverimg = cover_img
            data_save.bookfile = book
            data_save.price = price
            data_save.save()
            print("-" * 30, "book saved", "-" * 30)
            return redirect('bookupload')
        data = Book.objects.filter(username=request.user)
        return render(request, 'bookupload.html', {'yourbook': data})
    else:
        return redirect('login.html')
