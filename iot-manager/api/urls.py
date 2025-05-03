from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
	DeviceViewSet
)

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
# router.register(r'rules', ----, basename='rule')
# router.register(r'logs', ----, basename='log')

urlpatterns = [
	path('', include(router.urls)),
]