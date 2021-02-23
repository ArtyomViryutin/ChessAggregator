from rest_framework import decorators, filters, mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from datetime import datetime
from rest_framework.decorators import action
from .models import Tournament
from .permissions import IsOwnerOrReadOnly, IsTournamentOrganizerOrReadOnly, IsOrganizerOrReadOnly
from .serializers import ParticipationSerializer, TournamentSerializer, AnonymousParticipationSerializer


class TournamentModelViewSet(ModelViewSet):
    permission_classes = (IsOrganizerOrReadOnly,)
    serializer_class = TournamentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    queryset = Tournament.objects.all()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)


class ParticipantsViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    lookup_field = 'player_id'

    def get_queryset(self):
        tid = self.kwargs.get('tid')
        tournament = Tournament.objects.get(id=tid)
        queryset = tournament.participation_set
        return queryset

    def perform_create(self, serializer):
        tid = self.kwargs.get('tid')
        tournament = Tournament.objects.get(id=tid)
        serializer.save(player=self.request.user, tournament=tournament)


class AnonymousParticipationViewSet(ModelViewSet):
    permission_classes = (IsTournamentOrganizerOrReadOnly,)
    serializer_class = AnonymousParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        tid = self.kwargs.get('tid')
        tournament = Tournament.objects.get(id=tid)
        queryset = tournament.anonymous_participants
        return queryset

    def perform_create(self, serializer):
        tid = self.kwargs.get('tid')
        tournament = Tournament.objects.get(id=tid)
        serializer.save(tournament=tournament)
