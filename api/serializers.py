from rest_framework import serializers

from .models import Statistics


class StatisticsCreateSerializer(serializers.ModelSerializer):
    event_date = serializers.DateField(
        source="statistics.event_date", input_formats=["YYYY-MM-DD"]
    )

    class Meta:
        model = Statistics
        fields = ["event_date"]
