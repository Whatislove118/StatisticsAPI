import uuid

from django.db import models


# Create your models here.
class Statistics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_date = models.DateField(null=False, blank=False)
    views = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)
    cost = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)
