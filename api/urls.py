from rest_framework.routers import SimpleRouter

from .views import StatisticsViewSet

router = SimpleRouter()

router.register(r"statistics", StatisticsViewSet, basename="statistics")

urlpatterns = router.get_urls()
