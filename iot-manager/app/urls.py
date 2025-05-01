from django.urls import path
from .views import (
	IndexView,
	DeviceCreateView
)

urlpatterns = [
	path("", IndexView.as_view(), name="index"),
	path("device/create", DeviceCreateView.as_view(), name="device-create"),
]