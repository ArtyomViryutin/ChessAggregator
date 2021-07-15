from rest_framework import decorators, filters, mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Tournament
from rest_framework.response import Response
from .permissions import (IsParticipantOrReadOnly, IsTournamentOrganizerOrReadOnly,
                          IsOrganizerOrReadOnly)
from .serializers import TournamentSerializer
from rest_framework.decorators import action
from rest_framework import status
from .serializers import ParticipationSerializer, AnonymousParticipationSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class TournamentModelViewSet(ModelViewSet):
    permission_classes = (IsOrganizerOrReadOnly,)  # OK
    serializer_class = TournamentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    queryset = Tournament.objects.all()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'], url_path=r'(?P<tid>[0-9]+)/all-participants')
    def get_all_participants(self, request, tid):
        tournament = get_object_or_404(Tournament, id=tid)
        registered_participants = ParticipationSerializer(tournament.participation_set, many=True)
        anonymous_participants = AnonymousParticipationSerializer(tournament.anonymous_participants, many=True)
        return Response(anonymous_participants.data + registered_participants.data, status=status.HTTP_200_OK)


class ParticipantsViewSet(ModelViewSet):
    permission_classes = (IsParticipantOrReadOnly | IsTournamentOrganizerOrReadOnly,)  # OK
    serializer_class = ParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    lookup_field = 'user_id'

    def get_queryset(self):
        tid = self.kwargs.get('tid')
        tournament = get_object_or_404(Tournament, id=tid)
        queryset = tournament.participation_set
        return queryset

    def perform_create(self, serializer):
        tid = self.kwargs.get('tid')
        tournament = get_object_or_404(Tournament, id=tid)
        serializer.save(user=self.request.user, tournament=tournament)

    @action(detail=True, methods=['post'], url_path='add')
    def add_participant_by_id(self, request, tid, user_id):
        user = get_object_or_404(User, id=user_id)
        tournament = get_object_or_404(Tournament, id=tid)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user, tournament=tournament)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnonymousParticipationViewSet(ModelViewSet):
    permission_classes = (IsTournamentOrganizerOrReadOnly,)  # OK
    serializer_class = AnonymousParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        tid = self.kwargs.get('tid')
        tournament = get_object_or_404(Tournament, id=tid)
        queryset = tournament.anonymous_participants
        return queryset

    def perform_create(self, serializer):
        tid = self.kwargs.get('tid')
        tournament = get_object_or_404(Tournament, id=tid)
        serializer.save(tournament=tournament)
