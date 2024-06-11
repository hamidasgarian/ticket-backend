
from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Powered By Kaventador Development Team",
        default_version='v1',
        description="ashkboos",
        terms_of_service="https://ticket-team.ir/terms/",
        contact=openapi.Contact(email="info@jabarsing.ir"),
        license=openapi.License(name="jabaar"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/', include('core.urls')),
]
