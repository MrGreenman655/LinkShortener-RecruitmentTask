from django.urls import path

from api_v1.views import LinkShortenerApiView

app_name = "api_v1"
urlpatterns = [path("link-shortener/", LinkShortenerApiView.as_view(), name="link-shortener")]
