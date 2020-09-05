"""quick_interview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, re_path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/registration/', views.RegistrationView.as_view()),
    re_path('^api/v1/clients/(?P<id>.+)/$', views.ClientsView.as_view()),
    path('api/v1/clients/', views.ClientsView.as_view()),
    path('api/v1/clients/as_csv/', views.ClientsCSVView.as_view()),
    path('api/v1/clients/import/', views.ClientsCSVImportView.as_view()),
    re_path('^api/v1/products/(?P<id>.+)/$', views.ProductsView.as_view()),
    path('api/v1/products/', views.ProductsView.as_view()),
    re_path('^api/v1/bills/(?P<id>.+)/$', views.BillsView.as_view()),
    path('api/v1/bills/', views.BillsView.as_view())
]
