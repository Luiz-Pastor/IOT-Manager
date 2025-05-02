from django.urls import path
from .views import (
	IndexView,

	DeviceCreateView,
	DeviceListView,
	device_delete,
	DeviceDetailView,

	RuleCreateView
)

urlpatterns = [
	path("", IndexView.as_view(), name="index"),

	path("device/create", DeviceCreateView.as_view(), name="device-create"),
	path("device/list", DeviceListView.as_view(), name="device-list"),
	path("device/delete/<str:pk>", device_delete, name="device-delete"),
	path("device/<str:pk>", DeviceDetailView.as_view(), name="device-detail"),

	path("rule/create", RuleCreateView.as_view(), name='rule-create'),
]
