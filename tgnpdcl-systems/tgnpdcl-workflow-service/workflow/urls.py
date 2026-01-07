from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SanctionRequestViewSet

router = DefaultRouter()
router.register(r'requests', SanctionRequestViewSet, basename='sanction-request')

urlpatterns = [
    path('', include(router.urls)),
]
