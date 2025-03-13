
from django.urls import re_path, include
from django.urls import re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="storage",
        default_version='v1',
        description="storage description",
        contact=openapi.Contact(email="..."),
        license=openapi.License(name="..."),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^api/v1/', include('apps.urls')),

    re_path('doc/swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path('doc/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('doc/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

