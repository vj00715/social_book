from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name=""),
    path('login', views.login, name="loginUser"),
    path('logout', views.logout, name="logout"),
    path('register', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('authors_sellers', views.author_and_sellers, name="authors_sellers"),
    path('bookupload', views.bookupload, name="bookupload"),
    path('testing', views.testing, name="testing"),
    path('accessdata', views.accestokendatafetch, name='accessdata'),
    path('bookview', views.bookview, name="bookview"),
    path('showbook', views.showbook, name="showbook"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
