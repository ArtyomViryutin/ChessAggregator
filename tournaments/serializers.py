from djoser.serializers import UserSerializer
from rest_framework import serializers

from datetime import datetime
from .models import Participation, Tournament, AnonymousParticipation
from users.serializers import ProfileSerializer


class AnonymousParticipationSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = AnonymousParticipation
        fields = ['email', 'status', 'profile']

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile_serializer = ProfileSerializer(data=profile_data)
        profile_serializer.is_valid(raise_exception=True)
        profile = profile_serializer.save()
        return AnonymousParticipation.objects.create(profile=profile, **validated_data)


class TournamentSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    # participants = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # anonymous_participants = AnonymousParticipationSerializer(read_only=True, many=True)

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
