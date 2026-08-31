"""
URL routing for the enrollment app
"""

from rest_framework.routers import DefaultRouter

from .views import EnrollmentViewSet

app_name = "enrollments"

router = DefaultRouter()
router.register(r"", EnrollmentViewSet, basename="enrollment")

urlpatterns = router.urls
