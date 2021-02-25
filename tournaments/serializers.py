from rest_framework import serializers
from users.serializers import CustomUserSerializer
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

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = ProfileSerializer(instance=instance.profile, data=profile_data, partial=True)
        profile.is_valid(raise_exception=True)
        profile.save()
        return super(AnonymousParticipationSerializer, self).update(instance, validated_data)


class TournamentSerializer(serializers.ModelSerializer):
    organizer = serializers.PrimaryKeyRelatedField(read_only=True)
    # participants = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # anonymous_participants = AnonymousParticipationSerializer(read_only=True, many=True)

    class Meta:
        model = Tournament
        exclude = ['participants']


class ParticipationSerializer(serializers.ModelSerializer):
    player = CustomUserSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ['status', 'player']
