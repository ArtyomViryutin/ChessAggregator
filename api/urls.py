from django.urls import include, path
from .yasg import urlpatterns as doc_urls

urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('tournaments/', include('tournaments.urls')),
]

urlpatterns += doc_urls
