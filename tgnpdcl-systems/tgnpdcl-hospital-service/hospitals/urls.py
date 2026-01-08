from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HospitalViewSet, BillViewSet, BillListView, BillCreateView

router = DefaultRouter()
router.register(r'hospitals', HospitalViewSet)
router.register(r'bills', BillViewSet)

urlpatterns = [
    # API URLs
    path('api/', include(router.urls)),
    
    # Frontend URLs
    path('', BillListView.as_view(), name='bill_list'),
    path('create/', BillCreateView.as_view(), name='bill_create'),
]
