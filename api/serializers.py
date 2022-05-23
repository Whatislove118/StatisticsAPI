from rest_framework import serializers

from .models import Statistics


class StatisticsCreateSerializer(serializers.ModelSerializer):
    event_date = serializers.DateField(input_formats=["%Y-%m-%d"])

    class Meta:
        model = Statistics
        exclude = ["id", "views", "clicks"]
        extra_kwargs = {"cost": {"required": False}}


class StatisticsDetailsSerializer(serializers.ModelSerializer):
    cpc = serializers.FloatField()
    cpm = serializers.FloatField()

    class Meta:
        model = Statistics
        fields = "__all__"
        read_only_fields = ["id", "views", "clicks", "cpc", "cpm"]
