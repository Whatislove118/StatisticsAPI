from django.core.exceptions import FieldError
from django.db import models
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import serializers, viewsets
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response

from .models import Statistics
from .serializers import StatisticsCreateSerializer, StatisticsDetailsSerializer


@extend_schema(
    tags=["statistics"],
)
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter("from", OpenApiTypes.DATE, OpenApiParameter.QUERY),
            OpenApiParameter("to", OpenApiTypes.DATE, OpenApiParameter.QUERY),
            OpenApiParameter("order_by", OpenApiTypes.STR, OpenApiParameter.QUERY),
        ]
    )
)
class StatisticsViewSet(viewsets.GenericViewSet, CreateModelMixin, ListModelMixin):
    model = Statistics
    queryset = Statistics.objects.all()
    serializer_class = StatisticsDetailsSerializer

    def get_serializer_class(self):
        if self.action == "create":
            self.serializer_class = StatisticsCreateSerializer
        return super().get_serializer_class()

    @staticmethod
    def annotate_queryset(queryset):
        """
        Annotate queryset cpc & cpm data with catching ZeroDivision error.
        """
        return queryset.annotate(
            cpc=models.Case(
                models.When(clicks=0, then=0.00),
                default=models.F("cost") / models.F("clicks"),
                output_field=models.FloatField(),
            ),
        ).annotate(
            cpm=models.Case(
                models.When(views=0, then=0.00),
                default=models.F("cost") / models.F("views") * 1000,
                output_field=models.FloatField(),
            ),
        )

    def filter_queryset(self, queryset):
        queryset = self.get_queryset()

        date_from = self.request.query_params.get("from", None)
        date_to = self.request.query_params.get("to", None)

        if date_from:
            date_from = serializers.DateField(
                input_formats=["%Y-%m-%d"]
            ).to_internal_value(date_from)
            queryset = queryset.filter(event_date__gte=date_from)
        if date_to:
            date_to = serializers.DateField(
                input_formats=["%Y-%m-%d"]
            ).to_internal_value(date_to)
            queryset = queryset.filter(event_date__lte=date_to)
        return super().filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        self.queryset = self.annotate_queryset(self.queryset)
        order_by = self.request.query_params.get("order_by", None)
        # sorting after annotation because after this step, cpc and cpm a available for ordering
        if not order_by:
            order_by = "event_date"
        try:
            self.queryset = self.queryset.order_by(order_by)
        except FieldError:
            pass
        return super().list(request, *args, **kwargs)

    @extend_schema(
        methods=["DELETE"],
        request=None,
        responses={
            204: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                response_only=True,
                name="success",
                value={"detail": "Reseted"},
            )
        ],
    )
    @action(methods=["DELETE"], detail=False)
    def reset(self, request, *args, **kwargs):
        self.get_queryset().all().delete()
        return Response(data={"detail": "Reseted"}, status=204)
