import uuid

from django.db import models


class StatisticsManager(models.Manager):
    def extended_queryset(self):
        return self.get_queryset().annotate(
            cpc=models.F("cost") / models.F("clicks"),
            cpm=models.F("cost") / models.F("views") * 1000,
        )


class Statistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_date = models.DateField(null=False, blank=False)
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    class Meta:
        ordering = ["event_date"]
