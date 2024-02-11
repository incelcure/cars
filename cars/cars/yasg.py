from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Cars API",
        default_version='v1',
        description="Simple silly API with cars, Admin-role has permissions to post new cars, User can only get cars,"
                    "Project uses simplejwt tokens, soo in /login u can get this, use access token in headers to "
                    "do some stuff",
        terms_of_service="http://example.com/terms/",
        contact=openapi.Contact(email="sergeekoilia99@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]
