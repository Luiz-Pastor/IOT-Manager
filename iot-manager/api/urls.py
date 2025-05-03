from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
	DeviceViewSet,
	RuleViewSet,
	LogViewSet,
)

app_name = 'api'

router = DefaultRouter()
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'rules', RuleViewSet, basename='rule')
router.register(r'logs', LogViewSet, basename='log')

urlpatterns = [
	path('', include(router.urls)),
]