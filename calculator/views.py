from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from calculator.serializers import AirplaneModelSerializer


class AddAirplanes(APIView):
    """
    Add Airplanes by providing a list of airplane_id and passenger_count
    :param:
    [
        {
            "airplane_id": 1,
            "passengers_count": 30
        },
        {
            "airplane_id": 2,
            "passengers_count": 50
        }
    ]

    :returns:
    [
        {
            "airplane_id": 1,
            "passengers_count": 30,
            "fuel_consumption_per_minute": 0.06,
            "total_flight_time_in_minutes": 3333.3333333333335
        },
        {
            "airplane_id": 2,
            "passengers_count": 50,
            "fuel_consumption_per_minute": 0.1240823996531185,
            "total_flight_time_in_minutes": 3223.664283719766
        }
    ]
    """

    permission_classes = []  # Allow anyone to add airplane data
    authentication_classes = []  # No authentication applied on this API

    def post(self, request, *args, **kwargs):
        serializer = AirplaneModelSerializer(data=request.data, many=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
