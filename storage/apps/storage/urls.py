from rest_framework.routers import DefaultRouter
from apps.storage.views import ImageStorageViewSet

router = DefaultRouter()
router.register(r'image', ImageStorageViewSet)

urlpatterns = [

]

urlpatterns += router.urls
