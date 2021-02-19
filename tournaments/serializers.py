from djoser.serializers import UserSerializer
from rest_framework import serializers

from datetime import datetime
from .models import Participation, Tournament, AnonymousParticipation


class AnonymousParticipationSerializer(serializers.ModelSerializer):
    tournament = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AnonymousParticipation
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    # participants = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    anonymous_participants = AnonymousParticipationSerializer(read_only=True, many=True)

    class Meta:
        model = Tournament
        # fields = '__all__'
        exclude = ['participants']


class ParticipationSerializer(serializers.ModelSerializer):
    player = UserSerializer(read_only=True)
    tournament = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Participation
        fields = '__all__'
