from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login as auth_in, logout as auth_out
from .models import Book
from psycopg2 import connect
from sqlalchemy import create_engine
import pandas as pd
from django.contrib import messages
import requests

# SQLAlchemy create_engine
engine = create_engine(
    "postgresql://postgres:admin@localhost:5432/Markytics_test", echo=True
)

# getting default user model
User = get_user_model()
# Create your views here.


def home(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return redirect("login")


def signup(request):
    if request.method == "POST":
        mail = request.POST["mail"]
        print(mail)
        username = request.POST["username"]
        print(username)
        password = request.POST["password"]
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
        print("save")

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
    return redirect("loginUser")


def author_and_sellers(request):
    # authors_sellers
    data = User.objects.filter(public_visibility=True, is_superuser=False)
    return render(request, "basic-table.html", {"authors_sellers": data})


def book_ext_verify(book_name, cover_img_name):
    if book_name.split(".")[-1] == "pdf" and (
        cover_img_name.split(".")[-1] == "jpg"
        or cover_img_name.split(".")[-1] == "jpeg"
    ):
        return True
    else:
        return False


def bookupload(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST["title"]
            cover_img = request.FILES["coverimg"]
            book = request.FILES["book"]
            price = int(request.POST["price"])
            if book_ext_verify(book.name, cover_img.name):
                data_save = Book()
                data_save.username = request.user
                data_save.title = title
                data_save.coverimg = cover_img
                data_save.bookfile = book
                data_save.price = price
                data_save.save()
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    "Book Uploaded.........",
                    fail_silently=True,
                )
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    "Not Valid Extensions !!!!!.",
                    fail_silently=True,
                )
                # messages.error(request, "Not Valid Extensions !!!!!")
                print("Not Valid Extensions")
            print("-" * 30, "book saved", "-" * 30)
            return redirect("bookupload")
        data = Book.objects.filter(username=request.user)
        return render(request, "bookupload.html", {"yourbook": data})
    else:
        return redirect("login.html")


def showbook(request):
    data = Book.objects.all()
    return render(request, "showbook.html", {"allbook": data})


def bookwrapper(bookfunc):
    def datachecker(request):
        count = Book.objects.filter(username=request.user).count()
        if count > 0:
            return bookfunc(request)
        else:
            messages.add_message(request, messages.ERROR, "your have not book uploaded")
            return redirect("bookupload")

    return datachecker


@bookwrapper
def bookview(request):
    data = Book.objects.filter(username=request.user)
    return render(request, "bookview.html", {"yourbook": data})


def accestokendatafetch(request):
    # create token
    payload = {"username": "vaibhav123", "password": "jagtap123"}
    token = requests.post("http://127.0.0.1:8000/auth/token/login", data=payload)
    token = token.json()["auth_token"]

    # using token to fetch users data
    headers = {"Authorization": f"Token {token}"}
    data = requests.get("http://127.0.0.1:8000/auth/users/me", headers=headers)
    print("get data")
    print(data.json())

    # # to test logout
    # requests.post("http://127.0.0.1:8000/auth/token/logout", headers=headers)
    # print("logout")

    # data2 = requests.get("http://127.0.0.1:8000/auth/users/me", headers=headers)
    # print("get data 2")
    # print(data2.json())

    # # to fetch Book table
    # user_data = data.json()
    # try:
    #     book_data = Book.objects.filter(username_id=user_data['id'])
    #     if book_data.count() >= 1:
    #         print(book_data)
    #     else:
    #         raise Exception
    # except Exception:
    #     print("no data")
    return HttpResponse("<h1>Access data</h1>")


def testing(request):
    # using psycopg2 to fetch data
    print("-" * 30, "test is running", "-" * 30)
    conn = connect(
        dbname="Markytics_test",
        user="postgres",
        password="admin",
        host="localhost",
        port="5432",
    )
    cur = conn.cursor()
    q = "SELECT * FROM myapp_book"
    cur.execute(q)
    rows = cur.fetchall()
    for i in rows:
        print(i)
    cur.close()

    # using pandas
    # ------------------------------------- Good pratice This Really Life ------------------------------------------------
    queryset = User.objects.all()
    data = list(queryset.values("id", "username", "public_visibility"))
    # print(data)
    df = pd.DataFrame(data)[:3]

    #  Covert dataframe to dict
    df_dict = df.to_dict(
        orient="records"
    )  # this are values you can pass in orient('dict', 'list', 'series', 'split', 'records', 'index')
    print(df_dict)

    # ------------------------------------- ----------------------------- ------------------------------------------------
    # dicObj = {"id": [], "username": [], "email": [], "public_visibility": []}
    # for i in data:
    #     dicObj["id"].append(i.id)
    #     dicObj["username"].append(i.username)
    #     dicObj["email"].append(i.email)
    #     dicObj["public_visibility"].append(i.public_visibility)

    # df = pd.DataFrame(dicObj)  # .set_index('id')
    # print(df[2:5]) # to view rows in specific range
    # print(df.columns) # to get all columns name
    # print(df.username) # to print single column
    # print(df['username']) # to print single column
    # print(df[['username', 'email']]) # to print specific column

    # print(df[df['id'] > 4])
    # df.at[5, "username"] = 'vaibhav'  # change in data

    # dic = pd.DataFrame({'id': [5, 12], 'username': ['vaibhav', 'rahul'], 'email': ['mail@gmail.com', 'rmail@gmail.com'], 'public_visibility': [True, False]})
    # df = pd.concat([df, dic], ignore_index=True)
    # df.at[5, "username"] = 'xyz'  # change in data
    # print(df)

    # df.loc[10] = [5, "gogogo", "vj00715", True]
    # print(df)
    # print(df.sort_values('id'))

    # df['id'] = df['id'].replace(5, 55) # replace

    # print(df)
    return HttpResponse("<h1>testing</h1>")
