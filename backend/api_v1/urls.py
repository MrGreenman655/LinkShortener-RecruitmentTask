from rest_framework.routers import DefaultRouter

from api_v1.views import LinkApiViewSet

app_name = "api_v1"
urlpatterns = []

router = DefaultRouter()
router.register(r"links", LinkApiViewSet, basename="links")
urlpatterns += router.urls
