from rest_framework import serializers

from .models import Profile
from djoser.serializers import UserCreateSerializer, UserSerializer

from .parse import parse


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        fide_id = validated_data.pop('fide_id', None)
        frc_id = validated_data.pop('frc_id', None)
        if fide_id or frc_id:
            ratings = parse(frc_id=frc_id, fide_id=fide_id)
            validated_data.update(ratings)
        return super().update(instance, validated_data)


class CustomUserCreateSerializer(UserCreateSerializer):
    profile = ProfileSerializer()

    class Meta(UserCreateSerializer.Meta):
        fields = ['id', 'email', 'profile', 'password']

    def validate(self, attrs):
        return attrs


class CustomUserSerializer(UserSerializer):
    profile = ProfileSerializer()

    class Meta(UserSerializer.Meta):
        fields = ['id', 'email', 'is_organizer', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = ProfileSerializer(instance=instance.profile, data=profile_data, partial=True)
        profile.is_valid(raise_exception=True)
        profile.save()
        return super().update(instance, validated_data)
