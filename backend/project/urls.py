"""
URL configuration for project project.

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
from django.urls import path, include, reverse_lazy
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from project.views import HashRedirectView, HashNotFoundTemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api_v1.urls"), name="api_v1"),
    path(
        "api/v1/schema/",
        SpectacularAPIView.as_view(custom_settings={"SCHEMA_PATH_PREFIX": "/api/v1/"}),
        name="schema-v1",
    ),
    path("api/v1/docs/", SpectacularSwaggerView.as_view(url_name="schema-v1"), name="swagger-ui-v1"),
    path("<str:hash>", HashRedirectView.as_view(), name="main-redirect"),
    path("", RedirectView.as_view(url=reverse_lazy("swagger-ui-v1"))),
    path("hash-not-found/", HashNotFoundTemplateView.as_view(), name="hash_not_found"),
]
