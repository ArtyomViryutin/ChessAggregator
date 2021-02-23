from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import ParticipantsViewSet, TournamentModelViewSet, AnonymousParticipationViewSet

router = DefaultRouter()
router.register(r'', TournamentModelViewSet)
router.register(r'(?P<tid>[0-9]+)/participants',  ParticipantsViewSet, basename='participants')
router.register(r'(?P<tid>[0-9]+)/anonymous_participants',  AnonymousParticipationViewSet,
                basename='anonymous_participants')

urlpatterns = []

urlpatterns += router.urls
