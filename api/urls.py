from django.urls import include, path

urlpatterns = [
    path('users/', include('users.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('tournaments/', include('tournaments.urls')),
]
