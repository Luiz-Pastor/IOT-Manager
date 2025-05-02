from django.urls import path
from .views import (
	IndexView,

	DeviceCreateView,
	DeviceListView,
	device_delete,
	DeviceDetailView,

	RuleCreateView,
	RuleListView,
	rule_delete,
	RuleDetailView
)

urlpatterns = [
	path("", IndexView.as_view(), name="index"),

	path("device/create", DeviceCreateView.as_view(), name="device-create"),
	path("device/list", DeviceListView.as_view(), name="device-list"),
	path("device/delete/<str:pk>", device_delete, name="device-delete"),
	path("device/<str:pk>", DeviceDetailView.as_view(), name="device-detail"),

	path("rule/create", RuleCreateView.as_view(), name='rule-create'),
	path("rule/list", RuleListView.as_view(), name="rule-list"),
	path("rule/delete/<int:pk>", rule_delete, name="rule-delete"),
	path("rule/<int:pk>", RuleDetailView.as_view(), name="rule-detail"),
]
