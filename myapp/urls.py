from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login, name=""),
    path('login', views.login, name="login"),
    path('logout', views.logout, name="logout"),
    path('register', views.signup, name="signup"),
    path('home', views.home, name="home"),
    path('authors_sellers', views.author_and_sellers, name="authors_sellers"),
    path('bookupload', views.bookupload, name="bookupload"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
