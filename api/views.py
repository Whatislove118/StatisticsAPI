from rest_framework.viewsets import ModelViewSet
from .models import Statistics
from .serializers import StatisticsCreateSerializer


class StatisticsViewSet(ModelViewSet):
    model = Statistics
    queryset = Statistics.objects.all()
    serializer_class = StatisticsCreateSerializer

    def filter_queryset(self, queryset):

        return super().filter_queryset(queryset)
