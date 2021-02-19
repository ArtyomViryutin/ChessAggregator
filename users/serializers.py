from rest_framework import serializers

from .models import User


class PlayerSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['fide_id', 'frc_id', 'classic_fide_rating', 'rapid_fide_rating', 'blitz_fide_rating',
                  'classic_frc_rating', 'rapid_frc_rating', 'blitz_frc_rating', 'latin_name']
