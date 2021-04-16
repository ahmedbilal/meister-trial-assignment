"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from stats import views
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/login', views.LoginView.as_view(), name="login"),
    path('api/v1/logout', views.LogoutView.as_view(), name="logout"),
    path('api/v1/users/<int:pk>', views.UserView.as_view(), name="user_info"),
    path('api/v1/country_data', views.CountryList.as_view(), name="country_list"),
    path('api/v1/sales', views.SaleView.as_view(), name="sales"),
    path('api/v1/sale_statistics', views.StatisticsView.as_view(), name="statistics"),
    re_path(r"^.*$", views.react, name="home"),
]
