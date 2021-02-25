from rest_framework import decorators, filters, mixins, permissions
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from .models import Tournament
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly, IsTournamentOrganizerOrReadOnly, IsOrganizerOrReadOnly
from .serializers import ParticipationSerializer, TournamentSerializer, AnonymousParticipationSerializer
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework import status
from users.serializers import ProfileSerializer
from .serializers import ParticipationSerializer, AnonymousParticipationSerializer


def get_tournament_or_404(tid):
    try:
        tournament = Tournament.objects.get(id=tid)
    except Exception:
        raise NotFound(detail={'detail': f'Tournament with id={tid} does not exist.'})
    return tournament


class TournamentModelViewSet(ModelViewSet):
    permission_classes = (IsOrganizerOrReadOnly,)
    serializer_class = TournamentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    queryset = Tournament.objects.all()

    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated],
            url_path=r'(?P<tid>[0-9]+)/all-participants')
    def get_all_participants(self, request, tid):
        tournament = get_tournament_or_404(tid)
        registered_participants = ParticipationSerializer(tournament.participation_set, many=True)
        anonymous_participants = AnonymousParticipationSerializer(tournament.anonymous_participants, many=True)
        return Response(anonymous_participants.data + registered_participants.data, status=status.HTTP_200_OK)


class ParticipantsViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']
    lookup_field = 'player_id'

    def get_queryset(self):
        tid = self.kwargs.get('tid', 0)
        tournament = get_tournament_or_404(tid)
        queryset = tournament.participation_set
        return queryset

    def perform_create(self, serializer):
        tid = self.kwargs.get('tid')
        tournament = get_tournament_or_404(tid)
        serializer.save(player=self.request.user, tournament=tournament)


class AnonymousParticipationViewSet(ModelViewSet):
    permission_classes = (IsTournamentOrganizerOrReadOnly,)
    serializer_class = AnonymousParticipationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        tid = self.kwargs.get('tid')
        tournament = get_tournament_or_404(tid)
        queryset = tournament.anonymous_participants
        return queryset

    def perform_create(self, serializer):
        tid = self.kwargs.get('tid')
        tournament = get_tournament_or_404(tid)
        serializer.save(tournament=tournament)
