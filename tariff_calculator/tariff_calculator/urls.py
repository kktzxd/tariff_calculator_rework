"""
URL configuration for tariff_calculator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, reverse, re_path
from django.shortcuts import redirect
import calculator.views as views
from calculator.login import login_user, logout_user
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
app_name="Tariff_Calculator"
schema_view = get_schema_view(
    openapi.Info(
        title="Spam Filter API",
        default_version='v1',
        description="API для фильтрации спама",
        terms_of_service="https://example.com/terms/",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tariffs/', views.tariffs,name="tariffs"),
    path('save_tariff/', views.save_tariff),
    path('delete_tariff/<int:tariff_id>/',views.delete_tariff),
    path('calculator/', views.calculator_view, name="calculator"),
    path('get_payment_cost/',views.get_payment_cost),
    path("/", lambda request: redirect("calculator")),
    path("", lambda request: redirect("calculator")),
    path('login/', login_user, name="login"),
    path('logout/', logout_user, name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
