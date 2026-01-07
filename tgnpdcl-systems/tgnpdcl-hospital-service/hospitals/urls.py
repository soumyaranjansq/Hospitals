from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BillViewSet, LineItemViewSet

router = DefaultRouter()
router.register(r'bills', BillViewSet, basename='bill')
router.register(r'line-items', LineItemViewSet, basename='line-item')

urlpatterns = [
    path('', include(router.urls)),
]
