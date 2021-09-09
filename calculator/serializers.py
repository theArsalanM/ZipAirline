from django.contrib.auth.models import User
from rest_framework import serializers

from calculator.models import Airplane


class AirplaneModelSerializer(serializers.ModelSerializer):
    """
    Serializes Airplane JSON data submitted by user, and responds with 2 additional model fields of
    fuel_consumption_per_minute, and total_flight_time_in_minutes
    """
    fuel_consumption_per_minute = serializers.FloatField(read_only=True)
    total_flight_time_in_minutes = serializers.FloatField(read_only=True)
    added_by = serializers.RelatedField(queryset=User.objects.all(), write_only=True, required=False)

    class Meta:
        model = Airplane
        fields = (
            'airplane_id',
            'passengers_count',
            'added_by',
            'fuel_consumption_per_minute',
            'total_flight_time_in_minutes'
        )

    def create(self, validated_data):
        """
        Serializer's create method overwritten to save added_by parameter
        :param validated_data:
        :return: Airplane instance
        """
        user = self.context.get('request').user
        if user.is_authenticated:
            validated_data['added_by'] = user
        else:
            #  If user is not authenticated, added_by should be null
            # Our API is open for public, so there might be invalid data entered if client sends data in this key
            validated_data.pop('added_by', None)
        return super().create(validated_data)
