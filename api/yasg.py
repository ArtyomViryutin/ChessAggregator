from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path

schema_view = get_schema_view(
   openapi.Info(
      title="Chess Aggregator API",
      default_version='v1',
      description="API for the best mobile app - Chess Aggregator",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="virytinart1@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]