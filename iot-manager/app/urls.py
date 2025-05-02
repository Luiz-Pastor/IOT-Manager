from django.urls import path
from .views import (
	IndexView,
	DeviceCreateView,
	DeviceListView,
	device_delete
)

urlpatterns = [
	path("", IndexView.as_view(), name="index"),
	path("device/create", DeviceCreateView.as_view(), name="device-create"),
	path("device/list", DeviceListView.as_view(), name="device-list"),
	path("device/delete/<str:pk>", device_delete, name="device-delete"),
]
