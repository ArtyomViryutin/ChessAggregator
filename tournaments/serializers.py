from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Participation, Tournament, AnonymousParticipation
from users.serializers import ProfileSerializer

from django.forms.models import model_to_dict
from users.models import User


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

    class Meta:
        model = Tournament
        exclude = ['participants']


class ParticipationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Participation
        fields = ['status', 'user']

    def to_representation(self, instance):
        participation = model_to_dict(instance)
        participation.pop('tournament')
        participation.pop('id')
        uid = participation.pop('user')
        user = CustomUserSerializer(User.objects.get(id=uid))
        participation.update(user.data)
        return participation

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data
        user = self.context['request'].user
        tid = self.context['request'].parser_context.get('kwargs').get('tid')
        if Participation.objects.filter(user=user, tournament_id=tid):
            raise serializers.ValidationError({
                'detail': f'User {user} already participate in this tournament'
            })
        return data
