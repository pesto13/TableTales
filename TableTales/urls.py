"""
URL configuration for TableTales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
import restaurantsApp

urlpatterns = [
    path('admin/', admin.site.urls),

    #navbar
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("home/", TemplateView.as_view(template_name="home.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),

    #accounts
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),

    #restaurants
    path("restaurants/", include("restaurantsApp.urls")),

    #reviews
    path("restaurants/<int:pk>/reviews/", include("reviewsApp.urls")),

    #reservations
    path("restaurants/<int:pk>/reservations/", include("reservationsApp.urls")),

]
