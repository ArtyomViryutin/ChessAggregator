from rest_framework import decorators, filters, mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from datetime import datetime
from rest_framework.decorators import action
from .models import Tournament
from .permissions import IsOwnerOrReadOnly
from .serializers import ParticipationSerializer, TournamentSerializer


class TournamentModelViewSet(ModelViewSet):
    permission_classes = (IsOwnerOrReadOnly,)
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
